from bson import ObjectId
from random import randint

from common.mongo.data_types.keyword import Keyword
from common.config import SUPPORTED_LANGUAGES
from common.exceptions.parameters import UnsupportedLanguageError
from test.mongo.controller.setup import QueryTests


class QueriesKeywordTests(QueryTests):
    def setUp(self) -> None:
        super().setUp()
        self.load_sample_keyword()

    def test_set_deleted_flag(self):
        self.mongo_controller.keywords_collection.update_one(
            {"_id": self.keyword_sample._id}, {"$set": {"deleted": False}}
        )
        keyword = self.mongo_controller.get_keyword_by_id(
            self.keyword_sample._id, cast=False
        )
        self.assertFalse(keyword["deleted"], "Should be false initially")
        self.assertTrue(
            Keyword.from_dict(keyword).deleted, "The correct value should be true"
        )

        self.mongo_controller._set_deleted_flag(self.keyword_sample._id)

        keyword = self.mongo_controller.get_keyword_by_id(
            self.keyword_sample._id, cast=False
        )
        self.assertTrue(keyword["deleted"], "Should be set to deleted now")

    def test_add_keyword_unsupported_language(self):
        language = "some unsupported language"
        self.assertNotIn(
            language, SUPPORTED_LANGUAGES, "Make sure the language is not supported"
        )

        self.assertRaises(
            UnsupportedLanguageError,
            self.mongo_controller.add_keyword,
            self.keyword_sample.keyword_string,
            language,
            "some user",
        )

    def test_add_keyword_supported_language(self):
        language = SUPPORTED_LANGUAGES[0]
        self.assertIn(
            language, SUPPORTED_LANGUAGES, "Make sure the language is supported"
        )

        self.mongo_controller.add_keyword(
            self.keyword_sample.keyword_string, language, "some user"
        )

        self.assertTrue(
            True, "Make sure that we didn't throw an expcetion up until this point"
        )

    def test_add_keyword_new_keyword(self):
        keyword = self.keyword_new
        username = "some user"

        keyword_exists_check = self.mongo_controller.get_keyword(
            keyword.keyword_string, keyword.language
        )

        self.assertIsNone(
            keyword_exists_check, "Make sure the keyword isn't in the database yet"
        )
        self.assertNotIn(
            username,
            keyword.users,
            "Make sure the user is not yet associated to the keyword",
        )

        keyword_inserted = self.mongo_controller.add_keyword(
            keyword.keyword_string,
            keyword.language,
            username,
            return_object=True,
            cast=True,
        )
        self.assertEqual(
            keyword_inserted.keyword_string,
            keyword.keyword_string,
            "Make sure the correct keyword was inserted",
        )
        self.assertIn(
            username, keyword_inserted.users, "Make sure the user was added on creation"
        )

    def test_add_keyword_new_user(self):
        keyword = self.keyword_sample
        username = "some new user"

        self.assertNotIn(
            username,
            keyword.users,
            "Make sure the username is not yet added to the keyword",
        )

        keyword_updated = self.mongo_controller.add_keyword(
            keyword.keyword_string,
            keyword.language,
            username,
            return_object=True,
            cast=True,
        )

        self.assertEqual(
            keyword._id,
            keyword_updated._id,
            "The correct keyword should have been updated",
        )
        self.assertIn(
            username, keyword_updated.users, "The new user should have been added"
        )

    def test_get_keyword(self):
        keyword = self.mongo_controller.get_keyword(
            self.keyword_sample.keyword_string, self.keyword_sample.language
        )
        self.assertEqual(keyword, self.keyword_sample.to_json(cast_to_string_id=False))

    def test_get_keyword_user_allowed(self):
        username = "some user"
        self.mongo_controller.add_keyword(
            self.keyword_sample.keyword_string,
            self.keyword_sample.language,
            username=username,
        )
        keyword = self.mongo_controller.get_keyword(
            self.keyword_sample.keyword_string,
            self.keyword_sample.language,
            username=username,
            cast=True,
        )
        self.assertIsNotNone(keyword)
        self.assertIn(username, keyword.users)

    def test_get_keyword_user_not_allowed(self):
        username = "not an actual user"
        keyword = self.mongo_controller.get_keyword(
            self.keyword_sample.keyword_string,
            self.keyword_sample.language,
            username=username,
            cast=True,
        )
        self.assertIsNone(keyword)

    def test_get_keywords_user_no_keywords(self):
        username = "a user with no keywords"

        keywords = self.mongo_controller.get_keywords_user(username, cast=True)

        self.assertTrue(len(keywords) == 0, "No keywords should have been returned")

    def test_get_keywords_user_keywords(self):
        username = "some username"
        keywords = [self.keyword_sample, self.keyword_new]

        for keyword in keywords:
            keyword_added = self.mongo_controller.add_keyword(
                keyword.keyword_string,
                keyword.language,
                username,
                return_object=True,
                cast=True,
            )
            keyword._id = keyword_added._id

        keywords_returned = self.mongo_controller.get_keywords_user(username, cast=True)
        keywords_returned_ids = [keyword._id for keyword in keywords_returned]

        for keyword in keywords:
            self.assertIn(
                keyword._id,
                keywords_returned_ids,
                "All the keywords should have been returned",
            )

    def test_get_keyword_by_id_no_keyword(self):
        _id = ObjectId()

        keyword = self.mongo_controller.get_keyword_by_id(_id)

        self.assertIsNone(keyword, "No keyword should have been found")

    def test_get_keyword_by_id_keyword(self):
        keyword_existing = self.mongo_controller.get_keyword(
            self.keyword_sample.keyword_string, self.keyword_sample.language, cast=True
        )
        _id = keyword_existing._id

        keyword = self.mongo_controller.get_keyword_by_id(_id, cast=True)

        self.assertIsNotNone(keyword, "Should have found a keyword")
        self.assertEqual(_id, keyword._id, "The correct keyword should have been found")

    def test_delete_keyword_no_users(self):
        username = "some new user"
        keyword = self.keyword_sample

        self.assertNotIn(
            username, keyword.users, "Make sure the user is not associated yet"
        )

        deletion = self.mongo_controller.delete_keyword(keyword._id, username)

        self.assertEqual(
            deletion.modified_count, 0, "No keywords should have been modified"
        )

    def test_delete_keyword_users(self):
        username = "some new user"
        keyword = self.keyword_sample

        self.mongo_controller.add_keyword(
            keyword.keyword_string, keyword.language, username
        )

        deletion = self.mongo_controller.delete_keyword(keyword._id, username)

        self.assertEqual(
            deletion.modified_count, 1, "One keyword should have been updated"
        )

        keyword_after_deletion = self.mongo_controller.get_keyword_by_id(
            keyword._id, cast=True
        )

        self.assertNotIn(
            username,
            keyword_after_deletion.users,
            "The username should have been deleted",
        )

    def test_keywords_public_no_keywords(self):
        keywords = self.mongo_controller.get_keywords_public(cast=True)

        self.assertEqual(
            len(keywords), 0, "No keywords should have been found by default"
        )

    def test_keywords_public_keywords(self):
        _ids = [self.keyword_sample._id]

        self.mongo_controller.set_meta_keywords_public_ids(_ids)

        keywords = self.mongo_controller.get_keywords_public(cast=True)
        keywords_ids = [keyword._id for keyword in keywords]

        for _id in _ids:
            self.assertIn(
                _id, keywords_ids, "The public keywords should have been returned"
            )

    def test_keywords_public_invalid_id(self):
        _id = ObjectId()

        self.mongo_controller.set_meta_keywords_public_ids([_id])

        keywords = self.mongo_controller.get_keywords_public()

        self.assertEqual(len(keywords), 0, "No keywords should have been returned")

    def test_add_index_to_keyword_simple(self):
        keyword_id = self.keyword_sample._id
        index_id = ObjectId()

        keyword = self.mongo_controller.add_index_to_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertIn(
            index_id, keyword.indexes, "The correct index should have been added"
        )

    def test_add_index_to_keyword_duplicate_index(self):
        keyword_id = self.keyword_sample._id
        index_id = ObjectId()

        keyword = self.mongo_controller.add_index_to_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )
        length_initially = len(keyword.indexes)
        keyword = self.mongo_controller.add_index_to_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertIn(
            index_id, keyword.indexes, "The correct index should have been added"
        )
        self.assertEqual(
            len(keyword.indexes),
            length_initially,
            "The second index should have not been added",
        )

    def test_add_index_to_keyword_invalid_keyword(self):
        keyword_id = ObjectId()
        index_id = ObjectId()

        keyword = self.mongo_controller.add_index_to_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertIsNone(keyword, "No keyword should have been touched")

    def test_delete_index_from_keyword_no_index(self):
        keyword_id = self.keyword_sample._id
        index_id = ObjectId()

        keyword = self.mongo_controller.delete_index_from_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertEqual(
            keyword.indexes,
            self.keyword_sample.indexes,
            "No indexes should have been deleted",
        )

    def test_delete_index_from_keyword_index(self):
        keyword_id = self.keyword_sample._id
        index_id = ObjectId()

        keyword_initial = self.mongo_controller.add_index_to_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )
        self.assertIn(index_id, keyword_initial.indexes)

        keyword = self.mongo_controller.delete_index_from_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertNotIn(index_id, keyword.indexes, "Index should have been removed")
        self.assertEqual(
            len(keyword.indexes),
            len(keyword_initial.indexes) - 1,
            "Only one index should have been removed",
        )

    def test_delete_index_from_keyword_invalid_keyword(self):
        keyword_id = ObjectId()
        index_id = ObjectId()

        keyword = self.mongo_controller.delete_index_from_keyword(
            keyword_id, index_id, return_object=True, cast=True
        )

        self.assertIsNone(keyword, "No keyword should have been touched")

    def test_get_keywords_by_index_no_keywords(self):
        index_id = ObjectId()

        keywords = self.mongo_controller.get_keywords_by_index(index_id, cast=True)

        self.assertEqual(keywords, [], "No keywords should have been found")

    def test_get_keywords_by_index_keywords(self):
        index_id = ObjectId()
        keywords_amount = randint(1, 100)

        keywords = []
        for i in range(keywords_amount):
            keyword = self.mongo_controller.add_keyword(
                f"keyword {i}",
                SUPPORTED_LANGUAGES[0],
                "some user",
                return_object=True,
                cast=True,
            )
            keyword = self.mongo_controller.add_index_to_keyword(
                keyword._id, index_id, return_object=True
            )
            keywords.append(keyword)

        keywords_found = self.mongo_controller.get_keywords_by_index(index_id)

        self.assertEqual(
            len(keywords),
            len(keywords_found),
            "All the keywords should have been found",
        )
        self.assertEqual(
            keywords, keywords_found, "The correct keywords should have been found"
        )
