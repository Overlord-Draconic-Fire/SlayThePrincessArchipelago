from __future__ import annotations

from collections.abc import Mapping, Sequence
import typing
import enum
import warnings
from json import JSONEncoder, JSONDecoder

if typing.TYPE_CHECKING:
    from websockets import WebSocketServerProtocol as ServerConnection

from Utils import ByValue, Version

class ClientStatus(ByValue, enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30


class SlotType(ByValue, enum.IntFlag):
    spectator = 0b00
    player = 0b01
    group = 0b10

    @property
    def always_goal(self) -> bool:
        """Mark this slot as having reached its goal instantly."""
        return self.value != 0b01

class NetworkPlayer(typing.NamedTuple):
    """Represents a particular player on a particular team."""
    team: int
    slot: int
    alias: str
    name: str

class NetworkSlot(typing.NamedTuple):
    """Represents a particular slot across teams."""
    name: str
    game: str
    type: SlotType
    group_members: Sequence[int] = ()  # only populated if type == group


class NetworkItem(typing.NamedTuple):
    item: int
    location: int
    player: int
    """ Sending player, except in LocationInfo (from LocationScouts), where it is the receiving player. """
    flags: int = 0


_encode = JSONEncoder(ensure_ascii=False, check_circular=False, separators=(',', ':')).encode


def encode(obj: typing.Any) -> str:
    return _encode(_scan_for_TypedTuples(obj))


def _scan_for_TypedTuples(obj: typing.Any) -> typing.Any:
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # NamedTuple is not actually a parent class
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    if isinstance(obj, (tuple, list, set, frozenset)):
        return tuple(_scan_for_TypedTuples(o) for o in obj)
    if isinstance(obj, dict):
        return {key: _scan_for_TypedTuples(value) for key, value in obj.items()}
    return obj



def get_any_version(data: dict) -> Version:
    data = {key.lower(): value for key, value in data.items()}  # .NET version classes have capitalized keys
    return Version(int(data["major"]), int(data["minor"]), int(data["build"]))


allowlist = {
    "NetworkPlayer": NetworkPlayer,
    "NetworkItem": NetworkItem,
    "NetworkSlot": NetworkSlot,
}

custom_hooks = {
    "Version": get_any_version
}


def _object_hook(o: typing.Any) -> typing.Any:
    if isinstance(o, dict):
        hook = custom_hooks.get(o.get("class", None), None)
        if hook:
            return hook(o)
        cls = allowlist.get(o.get("class", None), None)
        if cls:
            for key in tuple(o):
                if key not in cls._fields:
                    del (o[key])
            return cls(**o)

    return o


decode = JSONDecoder(object_hook=_object_hook).decode


class Endpoint:
    __slots__ = ("socket",)

    socket: "ServerConnection"

    def __init__(self, socket):
        self.socket = socket
class _LocationStore:  # removed heavy implementation, kept placeholder for typing compatibility
    pass

class GamesPackage(typing.TypedDict, total=False):
    item_name_groups: dict[str, list[str]]
    item_name_to_id: dict[str, int]
    location_name_groups: dict[str, list[str]]
    location_name_to_id: dict[str, int]
    checksum: str


class DataPackage(typing.TypedDict):
    games: dict[str, GamesPackage]


if typing.TYPE_CHECKING:  # type-check with pure python implementation until we have a typing stub
    LocationStore = _LocationStore
else:
    try:
        from _speedups import LocationStore
        import _speedups
        import os.path
        if os.path.isfile("_speedups.pyx") and os.path.getctime(_speedups.__file__) < os.path.getctime("_speedups.pyx"):
            warnings.warn(f"{_speedups.__file__} outdated! "
                          f"Please rebuild with `cythonize -b -i _speedups.pyx` or delete it!")
    except ImportError:
        try:
            import pyximport
            pyximport.install()
        except ImportError:
            pyximport = None
        try:
            from _speedups import LocationStore
        except ImportError:
            warnings.warn("_speedups not available. Falling back to pure python LocationStore. "
                          "Install a matching C++ compiler for your platform to compile _speedups.")
            LocationStore = _LocationStore
