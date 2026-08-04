from __future__ import annotations

import asyncio
import concurrent.futures
import json
import typing
import builtins
import os
import itertools
import subprocess
import sys
import pickle
import functools
import io
import collections
import importlib
import logging
import warnings

from argparse import Namespace
from time import sleep
from typing import BinaryIO, Coroutine, Optional, Set, Dict, Any, Union
try:
    from typing import TypeGuard
except ImportError:
    TypeGuard = bool  # type: ignore  # Python 3.9 compatibility
from yaml import load, load_all, dump

try:
    from yaml import CLoader as UnsafeLoader, CSafeLoader as SafeLoader, CDumper as Dumper
except ImportError:
    from yaml import Loader as UnsafeLoader, SafeLoader, Dumper

if typing.TYPE_CHECKING:
    import tkinter
    import pathlib

def tuplize_version(version: str) -> Version:
    return Version(*(int(piece) for piece in version.split(".")))


class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int

    def as_simple_string(self) -> str:
        return ".".join(str(item) for item in self)


__version__ = "0.6.6"
version_tuple = tuplize_version(__version__)

is_macos = sys.platform == "darwin"

RetType = typing.TypeVar("RetType")
S = typing.TypeVar("S")
T = typing.TypeVar("T")


def cache_argsless(function: typing.Callable[[], RetType]) -> typing.Callable[[], RetType]:
    assert not function.__code__.co_argcount, "Can only cache 0 argument functions with this cache."

    sentinel = object()
    result: typing.Union[object, RetType] = sentinel

    def _wrap() -> RetType:
        nonlocal result
        if result is sentinel:
            result = function()
        return typing.cast(RetType, result)

    return _wrap


def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))


def local_path(*path: str) -> str:
    """
    Returns path to a file in the local Archipelago installation or source.
    This might be read-only and user_path should be used instead for ROMs, configuration, etc.
    """
    if hasattr(local_path, 'cached_path'):
        pass
    elif is_frozen():
        if hasattr(sys, "_MEIPASS"):
            # we are running in a PyInstaller bundle
            local_path.cached_path = sys._MEIPASS  # pylint: disable=protected-access,no-member
        else:
            # cx_Freeze
            local_path.cached_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        import __main__
        if globals().get("__file__") and os.path.isfile(__file__):
            # we are running in a normal Python environment
            local_path.cached_path = os.path.dirname(os.path.abspath(__file__))
        elif hasattr(__main__, "__file__") and os.path.isfile(__main__.__file__):
            # we are running in a normal Python environment, but AP was imported weirdly
            local_path.cached_path = os.path.dirname(os.path.abspath(__main__.__file__))
        else:
            # pray
            local_path.cached_path = os.path.abspath(".")

    return os.path.join(local_path.cached_path, *path)


def home_path(*path: str) -> str:
    """Returns path to a file in the user home's Archipelago directory."""
    if hasattr(home_path, 'cached_path'):
        pass
    elif sys.platform.startswith('linux'):
        xdg_data_home = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        home_path.cached_path = xdg_data_home + '/Archipelago'
        if not os.path.isdir(home_path.cached_path):
            legacy_home_path = os.path.expanduser('~/Archipelago')
            if os.path.isdir(legacy_home_path):
                os.renames(legacy_home_path, home_path.cached_path)
                os.symlink(home_path.cached_path, legacy_home_path)
            else:
                os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    elif sys.platform == 'darwin':
        import platformdirs
        home_path.cached_path = platformdirs.user_data_dir("Archipelago", False)
        os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    else:
        # not implemented
        home_path.cached_path = local_path()  # this will generate the same exceptions we got previously

    return os.path.join(home_path.cached_path, *path)


def user_path(*path: str) -> str:
    """Returns either local_path or home_path based on write permissions."""
    if hasattr(user_path, "cached_path"):
        pass
    elif os.access(local_path(), os.W_OK) and not (is_macos and is_frozen()):
        user_path.cached_path = local_path()
    else:
        user_path.cached_path = home_path()
        # populate home from local
        if user_path.cached_path != local_path():
            import filecmp
            if not os.path.exists(user_path("manifest.json")) or \
                    not os.path.exists(local_path("manifest.json")) or \
                    not filecmp.cmp(local_path("manifest.json"), user_path("manifest.json"), shallow=True):
                import shutil
                for dn in ("Players", "data/sprites", "data/lua"):
                    shutil.copytree(local_path(dn), user_path(dn), dirs_exist_ok=True)
                if not os.path.exists(local_path("manifest.json")):
                    warnings.warn(f"Upgrading {user_path()} from something that is not a proper install")
                else:
                    shutil.copy2(local_path("manifest.json"), user_path("manifest.json"))
            os.makedirs(user_path("worlds"), exist_ok=True)

    return os.path.join(user_path.cached_path, *path)


def cache_path(*path: str) -> str:
    """Returns path to a file in the user's Archipelago cache directory."""
    if hasattr(cache_path, "cached_path"):
        pass
    else:
        try:
            import platformdirs
            cache_path.cached_path = platformdirs.user_cache_dir("Archipelago", False)
        except ImportError:
            # Fallback if platformdirs is unavailable; use user_path to avoid hard crash
            warnings.warn("platformdirs unavailable; using user_path for cache")
            cache_path.cached_path = user_path(".archipelago_cache")

    return os.path.join(cache_path.cached_path, *path)

unsafe_parse_yaml = functools.partial(load, Loader=UnsafeLoader)

del load, load_all  # should not be used. don't leak their names


def persistent_store(category: str, key: str, value: typing.Any, force_store: bool = False):
    storage = persistent_load()
    if not force_store and category in storage and key in storage[category] and storage[category][key] == value:
        return  # no changes necessary
    category_dict = storage.setdefault(category, {})
    category_dict[key] = value
    path = user_path("_persistent_storage.yaml")
    with open(path, "wt") as f:
        f.write(dump(storage, Dumper=Dumper))


def persistent_load() -> Dict[str, Dict[str, Any]]:
    storage: Union[Dict[str, Dict[str, Any]], None] = getattr(persistent_load, "storage", None)
    if storage:
        return storage
    path = user_path("_persistent_storage.yaml")
    storage = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                storage = unsafe_parse_yaml(f.read())
        except Exception as e:
            logging.debug(f"Could not read store: {e}")
    if storage is None:
        storage = {}
    setattr(persistent_load, "storage", storage)
    return storage


def get_file_safe_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*')


def load_data_package_for_checksum(game: str, checksum: typing.Optional[str]) -> Dict[str, Any]:
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        path = cache_path("datapackage", get_file_safe_name(game), f"{checksum}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except Exception as e:
                logging.debug(f"Could not load data package: {e}")

    # fall back to old cache
    cache = persistent_load().get("datapackage", {}).get("games", {}).get(game, {})
    if cache.get("checksum") == checksum:
        return cache

    # cache does not match
    return {}


def store_data_package_for_checksum(game: str, data: typing.Dict[str, Any]) -> None:
    checksum = data.get("checksum")
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        game_folder = cache_path("datapackage", get_file_safe_name(game))
        os.makedirs(game_folder, exist_ok=True)
        try:
            with open(os.path.join(game_folder, f"{checksum}.json"), "w", encoding="utf-8-sig") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        except Exception as e:
            logging.debug(f"Could not store data package: {e}")


@cache_argsless
def get_unique_identifier():
    common_path = cache_path("common.json")
    try:
        with open(common_path) as f:
            common_file = json.load(f)
            uuid = common_file.get("uuid", None)
    except FileNotFoundError:
        common_file = {}
        uuid = None

    if uuid:
        return uuid

    from uuid import uuid4
    uuid = str(uuid4())
    common_file["uuid"] = uuid

    cache_folder = os.path.dirname(common_path)
    os.makedirs(cache_folder, exist_ok=True)
    with open(common_path, "w") as f:
        json.dump(common_file, f, separators=(",", ":"))
    return uuid


class KeyedDefaultDict(collections.defaultdict):
    """defaultdict variant that uses the missing key as argument to default_factory"""
    default_factory: typing.Callable[[typing.Any], typing.Any]

    def __init__(self,
                 default_factory: typing.Callable[[Any], Any] = None,
                 seq: typing.Union[typing.Mapping, typing.Iterable, None] = None,
                 **kwargs):
        if seq is not None:
            super().__init__(default_factory, seq, **kwargs)
        else:
            super().__init__(default_factory, **kwargs)

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value

loglevel_mapping = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}

_faf_tasks: "Set[asyncio.Task[typing.Any]]" = set()


def async_start(co: Coroutine[None, None, typing.Any], name: Optional[str] = None) -> None:
    """
    Use this to start a task when you don't keep a reference to it or immediately await it,
    to prevent early garbage collection. "fire-and-forget"
    """
    # https://docs.python.org/3.11/library/asyncio-task.html#asyncio.create_task
    # Python docs:
    # ```
    # Important: Save a reference to the result of [asyncio.create_task],
    # to avoid a task disappearing mid-execution.
    # ```
    # This implementation follows the pattern given in that documentation.

    task: asyncio.Task[typing.Any] = asyncio.create_task(co, name=name)
    _faf_tasks.add(task)
    task.add_done_callback(_faf_tasks.discard)
