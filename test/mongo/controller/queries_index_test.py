from bson import ObjectId

from common.exceptions.parameters import UnsupportedIndexTypeError
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
            self.index_sample_inserted.to_json(cast_to_string_id=False)
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

    def test_get_indexes_by_type_invalid_type(self):
        username = "some username"
        index_type_invalid = "some invalid type"

        self.assertRaises(
            UnsupportedIndexTypeError,
            self.mongo_controller.get_indexes_by_type,
            index_type_invalid,
            username,
        )

    def test_get_indexes_by_type_no_indexes(self):
        username = "some username"
        index_type = IndexTypes.COMPANY.value

        indexes = self.mongo_controller.get_indexes_by_type(
            index_type, username, cast=True
        )

        self.assertEqual(indexes, [])

    def test_get_indexes_by_type_indexes(self):
        username = "some username"
        index_type = IndexTypes.COMPANY.value

        index_added = self.mongo_controller.add_index(
            "some name", index_type, username, return_object=True
        )

        indexes_found = self.mongo_controller.get_indexes_by_type(index_type, username)

        self.assertEqual(len(indexes_found), 1, "Only one should have been found")
        self.assertEqual(
            indexes_found,
            [index_added],
            "The index found should be the same that was added",
        )

    def test_get_indexes_by_type_many_indexes(self):
        username = "some username"
        index_type = IndexTypes.COMPANY.value

        index_added_one = self.mongo_controller.add_index(
            "some name", index_type, username, return_object=True
        )
        index_added_two = self.mongo_controller.add_index(
            "some other name", index_type, username, return_object=True
        )

        indexes_found = self.mongo_controller.get_indexes_by_type(index_type, username)

        self.assertEqual(len(indexes_found), 2, "Both indexes should have been found")
        self.assertEqual(
            indexes_found,
            [index_added_one, index_added_two],
            "The correct indexes should have been found",
        )

    def test_get_indexes_by_type_many_types(self):
        username = "some username"
        index_type = IndexTypes.COMPANY.value
        index_type_other = IndexTypes.BRANCH.value

        index_added = self.mongo_controller.add_index(
            "some name", index_type, username, return_object=True
        )
        index_added_other = self.mongo_controller.add_index(
            "some other name", index_type_other, username, return_object=True
        )

        indexes_found = self.mongo_controller.get_indexes_by_type(index_type, username)

        self.assertEqual(len(indexes_found), 1, "Only one index should have been found")
        self.assertEqual(
            indexes_found, [index_added], "The correct index should have been found"
        )
        self.assertNotIn(
            index_added_other,
            indexes_found,
            "The other index should not have been found",
        )

    def test_get_indexes_no_indexes(self):
        indexes = self.mongo_controller.get_indexes("some unused username", cast=True)
        self.assertEqual(indexes, [], "No index should have been found")

    def test_get_indexes_one_index(self):
        username = "some username"
        index_created = self.mongo_controller.add_index(
            "some name", IndexTypes.COMPANY.value, username, return_object=True
        )

        indexes = self.mongo_controller.get_indexes(username)

        self.assertEqual(
            indexes, [index_created], "The created index should have been returned"
        )

    def test_get_indexes_many_indexes(self):
        username = "some username"
        index_created_one = self.mongo_controller.add_index(
            "index 1", IndexTypes.COMPANY.value, username, return_object=True
        )
        index_created_two = self.mongo_controller.add_index(
            "index 2", IndexTypes.COMPANY.value, username, return_object=True
        )
        index_created_noise = self.mongo_controller.add_index(
            "index noise",
            IndexTypes.COMPANY.value,
            "some other username",
            return_object=True,
        )

        indexes = self.mongo_controller.get_indexes(username)

        self.assertEqual(
            indexes,
            [index_created_one, index_created_two],
            "The created indexes should have been returned",
        )
        self.assertNotIn(
            index_created_noise, indexes, "The noise index should have been ignored"
        )
