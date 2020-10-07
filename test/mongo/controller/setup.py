from unittest import TestCase
from bson import ObjectId

from common.mongo.controller import MongoController
from common.mongo.data_types.keyword import Keyword
from common.config import SUPPORTED_LANGUAGES

DB_NAME = "apoa-unit-testing"


class QueryTests(TestCase):
    mongo_controller: MongoController

    # Keywords
    keyword_sample = Keyword(ObjectId(), "sample keyword", SUPPORTED_LANGUAGES[0])
    keyword_new = Keyword(
        ObjectId(), "some new keyword", SUPPORTED_LANGUAGES[0]
    )  # Don't insert by default
    keyword_noise = Keyword(ObjectId(), "some noise", SUPPORTED_LANGUAGES[0])

    def setUp(self) -> None:
        self.mongo_controller = MongoController(db_name=DB_NAME)

        # General setup
        self.mongo_controller.set_meta_keywords_public_ids([])

        # Insert some noise
        self.mongo_controller.keywords_collection.insert_one(
            self.keyword_noise.to_json(cast_to_string_id=False)
        )

    def tearDown(self) -> None:
        self.mongo_controller.client.drop_database(DB_NAME)

    def load_sample_keyword(self):
        self.mongo_controller.keywords_collection.insert_one(
            self.keyword_sample.to_json(cast_to_string_id=False)
        )
        return self.keyword_sample

    def load_crawls(self, crawls):
        self.mongo_controller.crawls_collection.insert_many(crawls)
