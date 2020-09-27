from test.mongo.controller.setup import QueryTests


class QueriesMetaTests(QueryTests):
    def setUp(self) -> None:
        super().setUp()
        self.mongo_controller.meta_collection.delete_many({})

    def test_is_meta_initialised_false(self):
        is_initialised = self.mongo_controller.is_meta_initialised()
        self.assertFalse(is_initialised, "Should not be initialised")

    def test_is_meta_initialised_true(self):
        self.mongo_controller.set_meta_keywords_public_ids([])

        is_initialised = self.mongo_controller.is_meta_initialised()
        self.assertTrue(is_initialised, "Should be initialised")