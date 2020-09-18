from bson import ObjectId


class Index:
    def __init__(self, _id: ObjectId, name: str, users: list, deleted: bool):
        self._id = _id
        self.name = name
        self.users = users
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
            dict_input["deleted"],
        )

    def to_json(self) -> dict:
        return {
            "_id": self._id if type(self._id) is not ObjectId else str(self._id),
            "name": self.name,
            "users": self.users,
            "deleted": self.deleted,
        }
