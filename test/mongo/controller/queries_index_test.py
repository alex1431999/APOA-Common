from bson import ObjectId

from common.mongo.data_types.index import Index
from test.mongo.controller.setup import QueryTests


class QueriesIndexTests(QueryTests):
    # User fixtures
    sample_user = ObjectId()

    # Index fixtures
    sample_index = Index(ObjectId(), "sample index", [], False)
    sample_index_inserted = Index(
        ObjectId(), "sample index inserted", [sample_user], False
    )

    def setUp(self) -> None:
        super().setUp()
        self.mongo_controller.indexes_collection.insert_one(
            self.sample_index_inserted.to_json()
        )

    def test_add_index_new_index(self):
        user = ObjectId()
        index = self.mongo_controller.add_index(
            self.sample_index.name, user, return_object=True, cast=True
        )

        self.assertEqual(
            index.name, self.sample_index.name, "the correct index was inserted"
        )
        self.assertIn(user, index.users, "the user was added")

    def test_add_index_new_user(self):
        user = ObjectId()
        user_new = ObjectId()
        self.mongo_controller.add_index(self.sample_index.name, user)
        index = self.mongo_controller.add_index(
            self.sample_index.name, user_new, return_object=True, cast=True
        )

        self.assertEqual(
            len(index.users),
            len(self.sample_index.users) + 2,
            "Only exactly 2 new users should have " "been added",
        )
        self.assertIn(user, index.users, "The old user wasn't deleted")
        self.assertIn(user_new, index.users, "The new user is part of users now")

    def test_get_index(self):
        index = self.mongo_controller.get_index(
            self.sample_index_inserted.name, cast=True
        )

        self.assertIsNotNone(index, "Should have found something")
        self.assertEqual(
            index._id,
            self.sample_index_inserted._id,
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
            self.sample_index_inserted._id, cast=True
        )

        self.assertEqual(
            index._id,
            self.sample_index_inserted._id,
            "The correct index should have been returned",
        )

    def test_get_index_by_id_no_index(self):
        index = self.mongo_controller.get_index_by_id(ObjectId())
        index_casted = self.mongo_controller.get_index_by_id(ObjectId(), cast=True)

        self.assertIsNone(index, "Should just be None")
        self.assertIsNone(index_casted, "Should just be None")
