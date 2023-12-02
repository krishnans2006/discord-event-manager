import os
from typing import Optional, Any

import google.cloud.firestore_v1
import firebase_admin as fb
from firebase_admin.firestore import firestore as FIRESTORE


cred = fb.credentials.Certificate(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "creds.json")
)
fb.initialize_app(cred)

db: google.cloud.firestore_v1.client.Client = fb.firestore.client()


class DB:
    """Basic database CRUD operations."""

    @staticmethod
    def s_d(coll: str, doc: str, obj: dict) -> None:
        db.collection(coll).document(doc).set(obj)

    @staticmethod
    def s_f(coll: str, doc: str, field: str, value: Any) -> None:
        return DB.u_d(coll, doc, {field: value})

    @staticmethod
    def g_d(coll: str, doc: str) -> dict | bool:
        doc_ref = db.collection(coll).document(doc).get()
        if not doc_ref.exists:
            return False
        return doc_ref.to_dict()

    @staticmethod
    def g_f(coll: str, doc: str, field: str) -> Any:
        doc_ref = db.collection(coll).document(doc).get({field})
        if not doc_ref.exists:
            return False
        return doc_ref.to_dict().get(field)

    @staticmethod
    def u_d(coll: str, doc: str, obj: dict) -> None:
        db.collection(coll).document(doc).update(obj)

    @staticmethod
    def u_f(coll: str, doc: str, field: str, value: Any) -> None:
        DB.u_d(coll, doc, {field: value})

    @staticmethod
    def d_d(coll: str, doc: str) -> None:
        db.collection(coll).document(doc).delete()

    @staticmethod
    def d_f(coll: str, doc: str, field: str) -> None:
        DB.u_d(coll, doc, {field: FIRESTORE.DELETE_FIELD})


class Collection:
    name: str

    @classmethod
    def create(cls, id_: str, obj: dict) -> bool:
        if cls.exists(id_):
            return False
        DB.s_d(cls.name, id_, obj)
        return True

    @classmethod
    def exists(cls, id_: str) -> bool:
        return bool(DB.g_d(cls.name, id_))

    @classmethod
    def get(cls, id_: str) -> dict | bool:
        return DB.g_d(cls.name, id_)

    @classmethod
    def update(cls, id_: str, obj: dict) -> bool:
        if not cls.exists(id_):
            return False
        DB.u_d(cls.name, id_, obj)
        return True

    @classmethod
    def delete(cls, id_: str) -> bool:
        # No need to check if it exists
        DB.d_d(cls.name, id_)
        return True


class SnowflakeCollection(Collection):
    @classmethod
    def create(cls, id_: int, obj: dict) -> bool:
        return super().create(str(id_), obj)

    @classmethod
    def exists(cls, id_: int) -> bool:
        return super().exists(str(id_))

    @classmethod
    def get(cls, id_: int) -> dict | bool:
        return super().get(str(id_))

    @classmethod
    def update(cls, id_: int, obj: dict) -> bool:
        return super().update(str(id_), obj)

    @classmethod
    def delete(cls, id_: int) -> bool:
        return super().delete(str(id_))


class User(SnowflakeCollection):
    name = "Users"

    @classmethod
    def create(cls, user_id: int, tag: str) -> bool:
        return super().create(user_id, {"ID": str(user_id), "Tag": tag})

    @classmethod
    def exists(cls, user_id: int, tag: Optional[str] = None) -> bool:
        found = super().exists(user_id)
        if not found:
            return False
        if tag:
            cls.update_tag(user_id, tag)
        return True

    @classmethod
    def get(cls, user_id: int, tag: Optional[str] = None) -> dict | bool:
        doc = super().get(user_id)
        if not doc:
            return False
        if tag:
            cls.update_tag(user_id, tag)
        return doc

    @classmethod
    def update(cls, user_id: int, obj: dict, tag: Optional[str] = None) -> bool:
        if tag:
            obj["Tag"] = tag
        return super().update(user_id, obj)

    @classmethod
    def update_tag(cls, user_id: int, tag: str) -> bool:
        return super().update(user_id, {"Tag": tag})

    @classmethod
    def create_and_update_tag(cls, user_id: int, tag: str) -> bool:
        if cls.exists(user_id, tag):
            return cls.update_tag(user_id, tag)
        else:
            return cls.create(user_id, tag)


class Event(SnowflakeCollection):
    name = "Events"

    @classmethod
    def add_interested(cls, event_id: int, users: dict[int, str]) -> bool:
        if not cls.exists(event_id):
            return False
        super().update(event_id, {"Interested": list(users.keys())})

        for user_id, tag in users.items():
            User.create_and_update_tag(user_id, tag)
