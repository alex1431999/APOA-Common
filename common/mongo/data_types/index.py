from bson import ObjectId
from enum import Enum


class IndexTypes(Enum):
    """
    Enumerate all the different index types
    """
    COMPANY = "COMPANY"
    COMPETITION = "COMPETITION"
    BRANCH = "BRANCH"
    MARKET = "MARKET"


class Index:
    def __init__(self, _id: ObjectId, name: str, users: list, index_type: IndexTypes, deleted: bool):
        self._id = _id
        self.name = name
        self.users = users
        self.index_type = index_type
        self.deleted = deleted

    @staticmethod
    def from_dict(dict_input: dict):
        if not dict_input:
            return None

        if dict_input["_id"] is ObjectId:
            _id = dict_input["_id"]
        else:
            _id = (ObjectId(dict_input["_id"]),)

        return Index(
            dict_input["_id"]
            if type(dict_input["_id"]) is ObjectId
            else ObjectId(dict_input["_id"]),
            dict_input["name"],
            dict_input["users"],
            dict_input["index_type"],
            dict_input["deleted"],
        )

    def to_json(self) -> dict:
        return {
            "_id": self._id if type(self._id) is not ObjectId else str(self._id),
            "name": self.name,
            "users": self.users,
            "index_type": self.index_type,
            "deleted": self.deleted,
        }
