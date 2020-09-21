from bson import ObjectId

from common.mongo.data_types.index import Index, IndexTypes
from test.mongo.controller.setup import QueryTests


class QueriesIndexTests(QueryTests):
    # username fixtures
    username_sample = ObjectId()

    # Index fixtures
    index_sample = Index(
        ObjectId(), "sample index", [], IndexTypes.COMPANY.value, False
    )
    index_sample_inserted = Index(
        ObjectId(),
        "sample index inserted",
        [username_sample],
        IndexTypes.COMPANY.value,
        False,
    )

    def setUp(self) -> None:
        super().setUp()
        self.mongo_controller.indexes_collection.insert_one(
            self.index_sample_inserted.to_json()
        )

    def test_add_index_new_index(self):
        username = "some username"
        index = self.mongo_controller.add_index(
            self.index_sample.name,
            IndexTypes.COMPANY.value,
            username,
            return_object=True,
            cast=True,
        )

        self.assertEqual(
            index.name, self.index_sample.name, "the correct index was inserted"
        )
        self.assertIn(username, index.users, "the username was added")

    def test_add_index_new_username(self):
        username = "some username"
        username_new = "some username new"
        self.mongo_controller.add_index(
            self.index_sample.name, IndexTypes.COMPANY.value, username
        )
        index = self.mongo_controller.add_index(
            self.index_sample.name,
            IndexTypes.COMPANY.value,
            username_new,
            return_object=True,
            cast=True,
        )

        self.assertEqual(
            len(index.users),
            len(self.index_sample.users) + 2,
            "Only exactly 2 new usernames should have " "been added",
        )
        self.assertIn(username, index.users, "The old username wasn't deleted")
        self.assertIn(
            username_new, index.users, "The new username is part of usernames now"
        )

    def test_get_index(self):
        index = self.mongo_controller.get_index(
            self.index_sample_inserted.name, cast=True
        )

        self.assertIsNotNone(index, "Should have found something")
        self.assertEqual(
            index._id,
            self.index_sample_inserted._id,
            "The correct index should have been returned",
        )

    def test_get_index_no_index(self):
        name = "this index doesn't exist"
        index = self.mongo_controller.get_index(name, cast=False)
        index_casted = self.mongo_controller.get_index(name, cast=True)

        self.assertIsNone(index, "Should just be None")
        self.assertIsNone(index_casted, "Should just be None")

    def test_get_index_by_id(self):
        index = self.mongo_controller.get_index_by_id(
            self.index_sample_inserted._id, cast=True
        )

        self.assertEqual(
            index._id,
            self.index_sample_inserted._id,
            "The correct index should have been returned",
        )

    def test_get_index_by_id_no_index(self):
        index = self.mongo_controller.get_index_by_id(ObjectId())
        index_casted = self.mongo_controller.get_index_by_id(ObjectId(), cast=True)

        self.assertIsNone(index, "Should just be None")
        self.assertIsNone(index_casted, "Should just be None")
