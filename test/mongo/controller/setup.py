from unittest import TestCase

from common.mongo.controller import MongoController

DB_NAME = 'apoa-unit-testing'

class QueryTests(TestCase):
    mongo_controller: MongoController

    def setUp(self) -> None:
        self.mongo_controller = MongoController(db_name=DB_NAME)

    def tearDown(self) -> None:
        self.mongo_controller.client.drop_database(DB_NAME)