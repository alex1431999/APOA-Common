from unittest import TestCase
from bson import ObjectId
from datetime import datetime, timedelta

from common.mongo.controller import MongoController
from common.mongo.data_types.keyword import Keyword
from common.mongo.data_types.crawling.crawl_result import CrawlResult, CrawlTypes
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

    # Keywords for crawls
    keyword_crawl_outdated = Keyword(
        ObjectId(), "associated to crawl_outdated one and two", SUPPORTED_LANGUAGES[0]
    )
    keyword_crawl_outdated_two = Keyword(
        ObjectId(), "associated to crawl_outdated three", SUPPORTED_LANGUAGES[0]
    )

    # Crawls
    crawl_outdated = CrawlResult(
        ObjectId(),
        keyword_crawl_outdated._id,
        keyword_crawl_outdated.keyword_string,
        keyword_crawl_outdated.language,
        "some text",
        datetime.now() - timedelta(days=400),
        crawl_type=CrawlTypes.TWITTER.value,
    )
    crawl_outdated_two = CrawlResult(
        ObjectId(),
        keyword_crawl_outdated._id,
        keyword_crawl_outdated.keyword_string,
        keyword_crawl_outdated.language,
        "some text",
        datetime.now() - timedelta(days=500),
        crawl_type=CrawlTypes.TWITTER.value,
    )
    crawl_outdated_three = CrawlResult(
        ObjectId(),
        keyword_crawl_outdated_two._id,
        keyword_crawl_outdated_two.keyword_string,
        keyword_crawl_outdated_two.language,
        "some text",
        datetime.now() - timedelta(days=600),
        crawl_type=CrawlTypes.TWITTER.value,
    )

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

    def load_keywords(self, keywords: list):
        keywords = [keyword.to_json(cast_to_string_id=False) for keyword in keywords]
        self.mongo_controller.keywords_collection.insert_many(keywords)

    def load_crawls(self, crawls: list):
        crawls = [crawl.to_json(cast_to_string_id=False) for crawl in crawls]
        self.mongo_controller.crawls_collection.insert_many(crawls)
