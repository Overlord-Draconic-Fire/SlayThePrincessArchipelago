from __future__ import annotations

import collections
import copy
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools
import warnings

import websockets

import Utils

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")

from NetUtils import Endpoint, decode, NetworkItem, encode, ClientStatus, NetworkSlot, SlotType
from Utils import Version, async_start
from worlds import network_data_package
import os
import ssl

logger = logging.getLogger("Client")

@Utils.cache_argsless
def get_ssl_context():
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

class CommonContext:
    # The following attributes are used to Connect and should be adjusted as needed in subclasses
    tags: typing.Set[str] = {"AP"}
    game: typing.Optional[str] = None
    items_handling: typing.Optional[int] = None
    want_slot_data: bool = True  # should slot_data be retrieved via Connect

    class NameLookupDict:
        """A specialized dict, with helper methods, for id -> name item/location data package lookups by game."""
        def __init__(self, ctx: CommonContext, lookup_type: typing.Literal["item", "location"]):
            self.ctx: CommonContext = ctx
            self.lookup_type: typing.Literal["item", "location"] = lookup_type
            self._unknown_item: typing.Callable[[int], str] = lambda key: f"Unknown {lookup_type} (ID: {key})"
            self._archipelago_lookup: typing.Dict[int, str] = {}
            self._game_store: typing.Dict[str, typing.ChainMap[int, str]] = collections.defaultdict(
                lambda: collections.ChainMap(self._archipelago_lookup, Utils.KeyedDefaultDict(self._unknown_item)))

        # noinspection PyTypeChecker
        def __getitem__(self, key: str) -> typing.Mapping[int, str]:
            assert isinstance(key, str), f"ctx.{self.lookup_type}_names used with an id, use the lookup_in_ helpers instead"
            return self._game_store[key]

        def __len__(self) -> int:
            return len(self._game_store)

        def __iter__(self) -> typing.Iterator[str]:
            return iter(self._game_store)

        def __repr__(self) -> str:
            return repr(self._game_store)

        def lookup_in_game(self, code: int, game_name: typing.Optional[str] = None) -> str:
            """Returns the name for an item/location id in the context of a specific game or own game if `game` is
            omitted.
            """
            if game_name is None:
                game_name = self.ctx.game
                assert game_name is not None, f"Attempted to lookup {self.lookup_type} with no game name available."

            return self._game_store[game_name][code]

        def lookup_in_slot(self, code: int, slot: typing.Optional[int] = None) -> str:
            """Returns the name for an item/location id in the context of a specific slot or own slot if `slot` is
            omitted.

            Use of `lookup_in_slot` should not be used when not connected to a server. If looking in own game, set
            `ctx.game` and use `lookup_in_game` method instead.
            """
            if slot is None:
                slot = self.ctx.slot
                assert slot is not None, f"Attempted to lookup {self.lookup_type} with no slot info available."

            return self.lookup_in_game(code, self.ctx.slot_info[slot].game)

        def update_game(self, game: str, name_to_id_lookup_table: typing.Dict[str, int]) -> None:
            """Overrides existing lookup tables for a particular game."""
            id_to_name_lookup_table = Utils.KeyedDefaultDict(self._unknown_item)
            id_to_name_lookup_table.update({code: name for name, code in name_to_id_lookup_table.items()})
            self._game_store[game] = collections.ChainMap(self._archipelago_lookup, id_to_name_lookup_table)
            if game == "Archipelago":
                # Keep track of the Archipelago data package separately so if it gets updated in a custom datapackage,
                # it updates in all chain maps automatically.
                self._archipelago_lookup.clear()
                self._archipelago_lookup.update(id_to_name_lookup_table)

    # defaults
    starting_reconnect_delay: int = 5
    current_reconnect_delay: int = starting_reconnect_delay
    ui: typing.Optional["kvui.GameManager"] = None
    ui_task: typing.Optional["asyncio.Task[None]"] = None
    input_task: typing.Optional["asyncio.Task[None]"] = None
    keep_alive_task: typing.Optional["asyncio.Task[None]"] = None
    server_task: typing.Optional["asyncio.Task[None]"] = None
    autoreconnect_task: typing.Optional["asyncio.Task[None]"] = None
    disconnected_intentionally: bool = False
    server: typing.Optional[Endpoint] = None
    server_version: Version = Version(0, 0, 0)
    generator_version: Version = Version(0, 0, 0)
    current_energy_link_value: typing.Optional[int] = None  # to display in UI, gets set by server
    max_size: int = 16*1024*1024  # 16 MB of max incoming packet size

    last_death_link: float = time.time()  # last send/received death link on AP layer

    # remaining type info
    slot_info: dict[int, NetworkSlot]
    """Slot Info from the server for the current connection"""
    server_address: typing.Optional[str]
    """Autoconnect address provided by the ctx constructor"""
    password: typing.Optional[str]
    """Password used for Connecting, expected by server_auth"""
    hint_cost: typing.Optional[int]
    """Current Hint Cost per Hint from the server"""
    hint_points: typing.Optional[int]
    """Current available Hint Points from the server"""
    player_names: dict[int, str]
    """Current lookup of slot number to player display name from server (includes aliases)"""

    finished_game: bool
    """
    Bool to signal that status should be updated to Goal after reconnecting
    to be used to ensure that a StatusUpdate packet does not get lost when disconnected
    """
    ready: bool
    """Bool to keep track of state for the /ready command"""
    team: typing.Optional[int]
    """Team number of currently connected slot"""
    slot: typing.Optional[int]
    """Slot number of currently connected slot"""
    auth: typing.Optional[str]
    """Name used in Connect packet"""
    seed_name: typing.Optional[str]
    """Seed name that will be validated on opening a socket if present"""

    # locations
    locations_checked: set[int]
    """
    Local container of location ids checked to signal that LocationChecks should be resent after reconnecting
    to be used to ensure that a LocationChecks packet does not get lost when disconnected
    """
    locations_scouted: set[int]
    """
    Local container of location ids scouted to signal that LocationScouts should be resent after reconnecting
    to be used to ensure that a LocationScouts packet does not get lost when disconnected
    """
    items_received: list[NetworkItem]
    """List of NetworkItems recieved from the server"""
    missing_locations: set[int]
    """Container of Locations that are unchecked per server state"""
    checked_locations: set[int]
    """Container of Locations that are checked per server state"""
    server_locations: set[int]
    """Container of Locations that exist per server state; a combination between missing and checked locations"""
    locations_info: dict[int, NetworkItem]
    """Dict of location id: NetworkItem info from LocationScouts request"""

    # data storage
    stored_data: dict[str, typing.Any]
    """
    Data Storage values by key that were retrieved from the server
    any keys subscribed to with SetNotify will be kept up to date
    """
    stored_data_notification_keys: set[str]
    """Current container of watched Data Storage keys, managed by ctx.set_notify"""

    # internals

    def __init__(self, server_address: typing.Optional[str] = None, password: typing.Optional[str] = None) -> None:
        # server state
        self.server_address = server_address
        self.username : str | None = None
        self.password = password
        self.hint_cost = None
        self.slot_info = {}
        self.permissions = {
            "release": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

        # own state
        self.finished_game = False
        self.ready = False
        self.team = None
        self.slot = None
        self.auth = None
        self.seed_name = None

        self.locations_checked = set()  # local state
        self.locations_scouted = set()
        self.items_received = []
        self.missing_locations = set()  # server state
        self.checked_locations = set()  # server state
        self.server_locations = set()  # all locations the server knows of, missing_location | checked_locations
        self.locations_info = {}

        # Persisted index of the last item that was already notified to the player
        self.last_notified_index: int = 0
        self._last_notified_loaded: bool = False

        self.stored_data = {}
        self.stored_data_notification_keys = set()

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        # game state
        self.player_names = {0: "Archipelago"}
        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()
        self._connect_sent = False

        # optional callbacks for host apps (e.g., Ren'Py)
        self.on_text_callback: typing.Optional[typing.Callable[[str], None]] = None
        self.on_json_callback: typing.Optional[typing.Callable[[typing.Any], None]] = None

        # Async loop reference (set when running inside asyncio.run in background thread)
        self.loop: typing.Optional[asyncio.AbstractEventLoop] = None

        self.item_names = self.NameLookupDict(self, "item")
        self.location_names = self.NameLookupDict(self, "location")
        self.checksums = {}

        if self.game:
            self.checksums[self.game] = network_data_package["games"][self.game]["checksum"]
        self.update_data_package(network_data_package)

        # execution
        self.keep_alive_task = asyncio.create_task(keep_alive(self), name="Bouncy")

    @property
    def suggested_address(self) -> str:
        if self.server_address:
            return self.server_address
        return Utils.persistent_load().get("client", {}).get("last_server_address", "")

    @property
    def total_locations(self) -> typing.Optional[int]:
        """Will return None until connected."""
        if self.checked_locations or self.missing_locations:
            return len(self.checked_locations | self.missing_locations)

    async def connection_closed(self):
        if self.server and self.server.socket is not None:
            await self.server.socket.close()
        self.reset_server_state()

    def reset_server_state(self):
        self.auth = None
        self.slot = None
        self.team = None
        self.items_received = []
        self.locations_info = {}
        self.server_version = Version(0, 0, 0)
        self.generator_version = Version(0, 0, 0)
        self.server = None
        self.server_task = None
        self.hint_cost = None
        self.permissions = {
            "release": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

    async def disconnect(self, allow_autoreconnect: bool = False):
        if not allow_autoreconnect:
            self.disconnected_intentionally = True
            if self.cancel_autoreconnect():
                logger.info("Cancelled auto-reconnect.")
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task is not None:
            await self.server_task
        if self.ui:
            self.ui.update_hints()

    async def send_msgs(self, msgs: typing.List[typing.Any]) -> None:
        """Send JSON-serializable messages if the websocket is alive."""
        if not self.server or not getattr(self.server, "socket", None):
            return
        sock = self.server.socket
        # websockets 15.x ClientConnection exposes `closed` but not `open`
        if getattr(sock, "closed", False):
            return
        await sock.send(encode(msgs))

    def consume_players_package(self, package: typing.List[tuple]):
        self.player_names = {slot: name for team, slot, name, orig_name in package if self.team == team}
        self.player_names[0] = "Archipelago"

    def event_invalid_slot(self):
        raise Exception('Invalid Slot; please verify that you have connected to the correct world.')

    def event_invalid_game(self):
        raise Exception('Invalid Game; please verify that you connected with the right game to the correct world.')

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            logger.error("Password required but not provided; aborting connection.")
            self.disconnected_intentionally = True
            if self.server and self.server.socket:
                await self.server.socket.close()
            return None

    async def get_username(self):
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.error("Slot name missing; cannot prompt in embedded mode.")
                self.disconnected_intentionally = True
                if self.server and self.server.socket:
                    await self.server.socket.close()
                return None

    async def send_connect(self, **kwargs: typing.Any) -> None:
        """
        Send a `Connect` packet to log in to the server,
        additional keyword args can override any value in the connection packet
        """
        payload = {
            'cmd': 'Connect',
            'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
            'tags': self.tags, 'items_handling': self.items_handling,
            'uuid': Utils.get_unique_identifier(), 'game': self.game, "slot_data": self.want_slot_data,
        }
        if kwargs:
            payload.update(kwargs)
        await self.send_msgs([payload])
        await self.send_msgs([{"cmd": "Get", "keys": ["_read_race_mode"]}])
        self._connect_sent = True

    async def check_locations(self, locations: typing.Collection[int]) -> set[int]:
        """Send new location checks to the server. Returns the set of actually new locations that were sent."""
        locations = set(locations) & self.missing_locations
        if locations:
            await self.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(locations)}])
        return locations

    async def connect(self, address: typing.Optional[str] = None) -> None:
        """ disconnect any previous connection, and open new connection to the server """
        await self.disconnect()
        self.server_task = asyncio.create_task(server_loop(self, address), name="server loop")

    async def message_loop(self) -> None:
        """Wait until the client is told to exit. Useful for embedding in other hosts."""
        await self.exit_event.wait()

    def cancel_autoreconnect(self) -> bool:
        if self.autoreconnect_task:
            self.autoreconnect_task.cancel()
            self.autoreconnect_task = None
            return True
        return False

    def slot_concerns_self(self, slot) -> bool:
        """Helper function to abstract player groups, should be used instead of checking slot == self.slot directly."""
        if slot == self.slot:
            return True
        if slot in self.slot_info:
            return self.slot in self.slot_info[slot].group_members
        return False

    def is_echoed_chat(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out messages sent by self."""
        return print_json_packet.get("type", "") == "Chat" \
            and print_json_packet.get("team", None) == self.team \
            and print_json_packet.get("slot", None) == self.slot

    def is_uninteresting_item_send(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out ItemSend prints that do not concern the local player."""
        return print_json_packet.get("type", "") == "ItemSend" \
            and not self.slot_concerns_self(print_json_packet["receiving"]) \
            and not self.slot_concerns_self(print_json_packet["item"].player)
    
    def is_connection_change(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out connection changes."""
        return print_json_packet.get("type", "") in ["Join","Part"]

    def on_print(self, args: dict):
        logger.info(args["text"])
        if self.on_text_callback:
            try:
                self.on_text_callback(args["text"])
            except Exception:
                logger.exception("on_text_callback failed")

    def on_print_json(self, args: dict):
        if self.ui:
            # send copy to UI
            self.ui.print_json(copy.deepcopy(args["data"]))

        if self.on_json_callback:
            try:
                self.on_json_callback(copy.deepcopy(args["data"]))
            except Exception:
                logger.exception("on_json_callback failed")

    def on_package(self, cmd: str, args: dict):
        """For custom package handling in subclasses."""
        pass

    def on_ui_command(self, text: str) -> None:
        """Gets called by kivy when the user executes a command starting with `/` or `!`.
        The command processor is still called; this is just intended for command echoing."""
        self.ui.print_json([{"text": text, "type": "color", "color": "orange"}])

    async def shutdown(self):
        self.server_address = ""
        self.username = None
        self.password = None
        self.cancel_autoreconnect()
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task:
            await self.server_task

        while self.input_requests > 0:
            self.input_queue.put_nowait(None)
            self.input_requests -= 1
        self.keep_alive_task.cancel()
        if self.ui_task:
            await self.ui_task
        if self.input_task:
            self.input_task.cancel()
    
    # DataPackage
    async def prepare_data_package(self, relevant_games: typing.Set[str],
                                remote_data_package_checksums: typing.Dict[str, str]):
        """Validate that all data is present for the current multiworld.
        Download, assimilate and cache missing data from the server."""
        # by documentation any game can use Archipelago locations/items -> always relevant
        relevant_games.add("Archipelago")

        needed_updates: typing.Set[str] = set()
        for game in relevant_games:
            if game not in remote_data_package_checksums:
                continue

            remote_checksum: typing.Optional[str] = remote_data_package_checksums.get(game)

            if not remote_checksum:  # custom data package and no checksum for this game
                needed_updates.add(game)
                continue

            cached_checksum: typing.Optional[str] = self.checksums.get(game)
            # no action required if cached version is new enough
            if remote_checksum != cached_checksum:
                local_checksum: typing.Optional[str] = network_data_package["games"].get(game, {}).get("checksum")
                if remote_checksum == local_checksum:
                    self.update_game(network_data_package["games"][game], game)
                else:
                    cached_game = Utils.load_data_package_for_checksum(game, remote_checksum)
                    cache_checksum: typing.Optional[str] = cached_game.get("checksum")
                    # download remote version if cache is not new enough
                    if remote_checksum != cache_checksum:
                        needed_updates.add(game)
                    else:
                        self.update_game(cached_game, game)
        if needed_updates:
            await self.send_msgs([{"cmd": "GetDataPackage", "games": [game_name]} for game_name in needed_updates])

    def update_game(self, game_package: dict, game: str):
        self.item_names.update_game(game, game_package["item_name_to_id"])
        self.location_names.update_game(game, game_package["location_name_to_id"])
        self.checksums[game] = game_package.get("checksum")

    def update_data_package(self, data_package: dict):
        for game, game_data in data_package["games"].items():
            self.update_game(game_data, game)

    def consume_network_data_package(self, data_package: dict):
        self.update_data_package(data_package)
        logger.info(f"Got new ID/Name DataPackage for {', '.join(data_package['games'])}")
        for game, game_data in data_package["games"].items():
            Utils.store_data_package_for_checksum(game, game_data)

    def consume_network_item_groups(self):
        data = {"item_name_groups": self.stored_data[f"_read_item_name_groups_{self.game}"]}
        current_cache = Utils.persistent_load().get("groups_by_checksum", {}).get(self.checksums[self.game], {})
        if self.game in current_cache:
            current_cache[self.game].update(data)
        else:
            current_cache[self.game] = data
        Utils.persistent_store("groups_by_checksum", self.checksums[self.game], current_cache)

    def consume_network_location_groups(self):
        data = {"location_name_groups": self.stored_data[f"_read_location_name_groups_{self.game}"]}
        current_cache = Utils.persistent_load().get("groups_by_checksum", {}).get(self.checksums[self.game], {})
        if self.game in current_cache:
            current_cache[self.game].update(data)
        else:
            current_cache[self.game] = data
        Utils.persistent_store("groups_by_checksum", self.checksums[self.game], current_cache)

    # data storage

    def set_notify(self, *keys: str) -> None:
        """Subscribe to be notified of changes to selected data storage keys.

        The values can be accessed via the "stored_data" attribute of this context, which is a dictionary mapping the
        names of the data storage keys to the latest values received from the server.
        """
        if new_keys := (set(keys) - self.stored_data_notification_keys):
            self.stored_data_notification_keys.update(new_keys)
            async_start(self.send_msgs([{"cmd": "Get",
                                        "keys": list(new_keys)},
                                        {"cmd": "SetNotify",
                                        "keys": list(new_keys)}]))

    # DeathLink hooks

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")

    async def send_death(self, death_text: str = ""):
        """Helper function to send a deathlink using death_text as the unique death cause string."""
        if self.server and self.server.socket:
            logger.info("DeathLink: Sending death to your friends...")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.player_names[self.slot],
                    "cause": death_text
                }
            }])

    async def update_death_link(self, death_link: bool):
        """Helper function to set Death Link connection tag on/off and update the connection if already connected."""
        old_tags = self.tags.copy()
        if death_link:
            self.tags.add("DeathLink")
        else:
            self.tags -= {"DeathLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    def handle_connection_loss(self, msg: str) -> None:
        """Helper for logging a loss of connection. Must be called from an except block."""
        exc_info = sys.exc_info()
        logger.exception(msg, exc_info=exc_info, extra={'compact_gui': True})

async def keep_alive(ctx: CommonContext, seconds_between_checks=100):
    """some ISPs/network configurations drop TCP connections if no payload is sent (ignore TCP-keep-alive)
    so we send a payload to prevent drop and if we were dropped anyway this will cause an auto-reconnect."""
    seconds_elapsed = 0
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)  # short sleep to not block program shutdown
        if ctx.server and ctx.slot:
            seconds_elapsed += 1
            if seconds_elapsed > seconds_between_checks:
                await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot]}])
                seconds_elapsed = 0

async def server_loop(ctx: CommonContext, address: typing.Optional[str] = None) -> None:
    if ctx.server and ctx.server.socket:
        logger.error('Already connected')
        return

    if address is None:  # set through CLI or APBP
        address = ctx.server_address

    # Wait for the user to provide a multiworld server address
    if not address:
        logger.info('Please connect to an Archipelago server.')
        return

    ctx.cancel_autoreconnect()

    address = f"ws://{address}" if "://" not in address \
        else address.replace("archipelago://", "ws://")

    server_url = urllib.parse.urlparse(address)
    if server_url.username:
        ctx.username = urllib.parse.unquote(server_url.username)
    if server_url.password:
        ctx.password = urllib.parse.unquote(server_url.password)

    def reconnect_hint() -> str:
        return ", type /connect to reconnect" if ctx.server_address else ""

    logger.info(f'Connecting to Archipelago server at {address}')
    try:
        port = server_url.port or 38281  # raises ValueError if invalid
        socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None,
                                        ssl=get_ssl_context() if address.startswith("wss://") else None,
                                        max_size=ctx.max_size)
        if ctx.ui is not None:
            ctx.ui.update_address_bar(server_url.netloc)
        ctx.server = Endpoint(socket)
        logger.info('Connected')
        ctx.server_address = address
        ctx.current_reconnect_delay = ctx.starting_reconnect_delay
        ctx.disconnected_intentionally = False
        async for data in ctx.server.socket:
            for msg in decode(data):
                await process_server_cmd(ctx, msg)
        logger.warning(f"Disconnected from multiworld server{reconnect_hint()}")
    except websockets.InvalidMessage:
        # probably encrypted or not an AP server; avoid crashing
        if address.startswith("ws://"):
            # try wss
            await server_loop(ctx, "ws" + address[1:])
        else:
            ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
                                    f"{reconnect_hint()}")
    except ConnectionRefusedError:
        ctx.handle_connection_loss("Connection refused by the server. "
                                "May not be running Archipelago on that address or port.")
    except websockets.InvalidURI:
        ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
    except OSError:
        ctx.handle_connection_loss("Failed to connect to the multiworld server")
    except Exception:
        ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
    finally:
        await ctx.connection_closed()
        if ctx.server_address and ctx.username and not ctx.disconnected_intentionally:
            logger.info(f"... automatically reconnecting in {ctx.current_reconnect_delay} seconds")
            if ctx.autoreconnect_task is None:
                ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(ctx), name="server auto reconnect")
        ctx.current_reconnect_delay *= 2

async def server_autoreconnect(ctx: CommonContext):
    await asyncio.sleep(ctx.current_reconnect_delay)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

async def process_server_cmd(ctx: CommonContext, args: dict):
    try:
        cmd = args["cmd"]
    except Exception:
        logger.exception(f"Could not get command from {args}")
        return
    
    logger.info(f"[process_server_cmd] Received command: {cmd}")
    
    if cmd == 'RoomInfo':
        if ctx.seed_name and ctx.seed_name != args["seed_name"]:
            msg = "The server is running a different multiworld than your client is. (invalid seed_name)"
            logger.error(msg)
        else:
            logger.info('--------------------------------')
            logger.info('Room Information:')
            logger.info('--------------------------------')
            version = args["version"]
            ctx.server_version = Version(*version)

            if "generator_version" in args:
                ctx.generator_version = Version(*args["generator_version"])
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'generator version: {ctx.generator_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            else:
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            if args['password']:
                logger.info('Password required')
            logger.info(
                f"A !hint costs {args['hint_cost']}% of your total location count as points"
                f" and you get {args['location_check_points']}"
                f" for each location checked. Use !hint for more information.")
            ctx.hint_cost = int(args['hint_cost'])
            ctx.check_points = int(args['location_check_points'])

            if "players" in args:  # TODO remove when servers sending this are outdated
                players = args.get("players", [])
                if len(players) < 1:
                    logger.info('No player connected')
                else:
                    players.sort()
                    current_team = -1
                    logger.info('Connected Players:')
                    for network_player in players:
                        if network_player.team != current_team:
                            logger.info(f'  Team #{network_player.team + 1}')
                            current_team = network_player.team
                        logger.info('    %s (Player %d)' % (network_player.alias, network_player.slot))

            # update data package
            data_package_checksums = args.get("datapackage_checksums", {})
            logger.info(f"[RoomInfo] Preparing data package, games: {set(args['games'])}")
            await ctx.prepare_data_package(set(args["games"]), data_package_checksums)
            logger.info(f"[RoomInfo] Data package prepared, calling server_auth")
            await ctx.server_auth(args['password'])
            logger.info(f"[RoomInfo] server_auth completed")

    elif cmd == 'DataPackage':
        ctx.consume_network_data_package(args['data'])

    elif cmd == 'ConnectionRefused':
        errors = args["errors"]
        if 'InvalidSlot' in errors:
            ctx.disconnected_intentionally = True
            ctx.event_invalid_slot()
        elif 'InvalidGame' in errors:
            ctx.disconnected_intentionally = True
            ctx.event_invalid_game()
        elif 'IncompatibleVersion' in errors:
            ctx.disconnected_intentionally = True
            raise Exception('Server reported your client version as incompatible. '
                            'This probably means you have to update.')
        elif 'InvalidItemsHandling' in errors:
            raise Exception('The item handling flags requested by the client are not supported')
        # last to check, recoverable problem
        elif 'InvalidPassword' in errors:
            logger.error('Invalid password')
            ctx.password = None
            await ctx.server_auth(True)
        elif errors:
            raise Exception("Unknown connection errors: " + str(errors))
        else:
            raise Exception('Connection refused by the multiworld host, no reason provided')

    elif cmd == 'Connected':
        ctx.username = ctx.auth
        ctx.team = args["team"]
        ctx.slot = args["slot"]

        # Reset per-slot notification tracking so the next ReceivedItems load pulls the right persisted index
        ctx._last_notified_loaded = False
        ctx.last_notified_index = 0

        # int keys get lost in JSON transfer
        ctx.slot_info = {0: NetworkSlot("Archipelago", "Archipelago", SlotType.player)}
        ctx.slot_info.update({int(pid): data for pid, data in args["slot_info"].items()})
        ctx.hint_points = args.get("hint_points", 0)
        ctx.consume_players_package(args["players"])
        ctx.stored_data_notification_keys.add(f"_read_hints_{ctx.team}_{ctx.slot}")
        if ctx.game:
            game = ctx.game
        else:
            game = ctx.slot_info[ctx.slot][1]
        ctx.stored_data_notification_keys.add(f"_read_item_name_groups_{game}")
        ctx.stored_data_notification_keys.add(f"_read_location_name_groups_{game}")
        msgs = []
        if ctx.locations_checked:
            msgs.append({"cmd": "LocationChecks",
                        "locations": list(ctx.locations_checked)})
        if ctx.locations_scouted:
            msgs.append({"cmd": "LocationScouts",
                        "locations": list(ctx.locations_scouted)})
        if ctx.stored_data_notification_keys:
            msgs.append({"cmd": "Get",
                        "keys": list(ctx.stored_data_notification_keys)})
            msgs.append({"cmd": "SetNotify",
                        "keys": list(ctx.stored_data_notification_keys)})
        if msgs:
            await ctx.send_msgs(msgs)
        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        # Get the server side view of missing as of time of connecting.
        # This list is used to only send to the server what is reported as ACTUALLY Missing.
        # This also serves to allow an easy visual of what locations were already checked previously
        # when /missing is used for the client side view of what is missing.
        ctx.missing_locations = set(args["missing_locations"])
        ctx.checked_locations = set(args["checked_locations"])
        ctx.server_locations = ctx.missing_locations | ctx. checked_locations

        server_url = urllib.parse.urlparse(ctx.server_address)
        Utils.persistent_store("client", "last_server_address", server_url.netloc)
        Utils.persistent_store("client", "last_slot_name", ctx.auth or ctx.username or "")

    elif cmd == 'ReceivedItems':
        start_index = args["index"]

        # Load last notified index once per session (per slot)
        if start_index == 0 and not ctx._last_notified_loaded:
            slot_key = ctx.auth or ctx.username or "default"
            stored = Utils.persistent_load().get("client", {}).get(f"last_notified_index::{slot_key}", 0)
            ctx.last_notified_index = int(stored)
            ctx._last_notified_loaded = True
            logger.info(f"[ReceivedItems] Loaded last_notified_index={ctx.last_notified_index} for slot_key={slot_key}")

        # Suppress user-facing notifications only for items already notified
        suppress_notify_threshold = ctx.last_notified_index

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            return
        if start_index == len(ctx.items_received):
            for offset, item in enumerate(args['items']):
                absolute_index = start_index + offset
                net_item = NetworkItem(*item)
                ctx.items_received.append(net_item)
                should_notify = absolute_index >= suppress_notify_threshold and hasattr(ctx, "item_received")
                logger.info(f"[ReceivedItems] Item index={absolute_index}, threshold={suppress_notify_threshold}, notify={should_notify}")
                if should_notify:
                    ctx.item_received(net_item)
        ctx.watcher_event.set()

        # Persist the new high-water mark for notifications
        if ctx._last_notified_loaded:
            ctx.last_notified_index = len(ctx.items_received)
            slot_key = ctx.auth or ctx.username or "default"
            Utils.persistent_store("client", f"last_notified_index::{slot_key}", ctx.last_notified_index)
            logger.info(f"[ReceivedItems] Saved last_notified_index={ctx.last_notified_index} for slot_key={slot_key}")

    elif cmd == 'LocationInfo':
        for item in [NetworkItem(*item) for item in args['locations']]:
            ctx.locations_info[item.location] = item
        ctx.watcher_event.set()

    elif cmd == "RoomUpdate":
        if "players" in args:
            ctx.consume_players_package(args["players"])
        if "hint_points" in args:
            ctx.hint_points = args['hint_points']
        if "checked_locations" in args:
            checked = set(args["checked_locations"])
            ctx.checked_locations |= checked
            ctx.missing_locations -= checked

    elif cmd == 'Print':
        ctx.on_print(args)

    elif cmd == 'PrintJSON':
        ctx.on_print_json(args)

    elif cmd == 'InvalidPacket':
        logger.warning(f"Invalid Packet of {args['type']}: {args['text']}")

    elif cmd == "Bounced":
        tags = args.get("tags", [])
        # we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been send this
        if "DeathLink" in tags and ctx.last_death_link != args["data"]["time"]:
            ctx.on_deathlink(args["data"])

    elif cmd == "Retrieved":
        ctx.stored_data.update(args["keys"])
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" in args["keys"]:
            ctx.ui.update_hints()
        if f"_read_item_name_groups_{ctx.game}" in args["keys"]:
            ctx.consume_network_item_groups()
        if f"_read_location_name_groups_{ctx.game}" in args["keys"]:
            ctx.consume_network_location_groups()

    elif cmd == "SetReply":
        ctx.stored_data[args["key"]] = args["value"]
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" == args["key"]:
            ctx.ui.update_hints()
        elif f"_read_item_name_groups_{ctx.game}" == args["key"]:
            ctx.consume_network_item_groups()
        elif f"_read_location_name_groups_{ctx.game}" == args["key"]:
            ctx.consume_network_location_groups()
        elif args["key"].startswith("EnergyLink"):
            ctx.current_energy_link_value = args["value"]
            if ctx.ui:
                ctx.ui.set_new_energy_link_value()
    else:
        logger.debug(f"unknown command {cmd}")

    ctx.on_package(cmd, args)
