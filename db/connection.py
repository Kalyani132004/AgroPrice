""" Manages the MongoDB database connection and provides collection access. """
import sys
import threading

from django.conf import settings

_lock = threading.Lock()
_client = None
_db = None
_using_mock = False


def _connect():
    global _client, _db, _using_mock
    try:
        import pymongo
        candidate = pymongo.MongoClient(
            settings.MONGO_URI, serverSelectionTimeoutMS=1500
        )
        candidate.admin.command("ping")  # forces a real connection check
        _client = candidate
        _db = _client[settings.MONGO_DB_NAME]
        _using_mock = False
        print("[AgroPrice] Connected to real MongoDB at", settings.MONGO_URI, file=sys.stderr)
    except Exception as exc:  # noqa: BLE001 - any connection failure -> fallback
        import mongomock
        _client = mongomock.MongoClient()
        _db = _client[settings.MONGO_DB_NAME]
        _using_mock = True
        print(
            f"[AgroPrice] MongoDB unreachable ({exc.__class__.__name__}: {exc}). "
            f"Falling back to in-memory mongomock for this session.",
            file=sys.stderr,
        )


def get_db():
    global _db
    if _db is None:
        with _lock:
            if _db is None:
                _connect()
    return _db


def is_using_mock() -> bool:
    get_db()
    return _using_mock


def get_collection(name: str):
    return get_db()[name]
