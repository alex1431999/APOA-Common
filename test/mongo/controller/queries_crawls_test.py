from bson import ObjectId
from datetime import datetime, timedelta

from common.mongo.data_types.keyword import Keyword
from common.mongo.data_types.crawling.crawl_results.news_result import NewsResult
from test.mongo.controller.setup import QueryTests


def generate_crawls(
    keyword: Keyword, amount: int, cast_to_json=True, time_difference=120
):
    crawls = [
        NewsResult(
            ObjectId(),
            keyword._id,
            keyword.keyword_string,
            keyword.language,
            f"some title {i}",
            f"some author {i}",
            f"some text {i}",
            datetime.now() - timedelta(minutes=time_difference * i),
            score=1,
        )
        for i in range(amount)
    ]
    if cast_to_json:
        crawls = [crawl.to_json(cast_to_string_id=False) for crawl in crawls]
    return crawls


class QueriesCrawlsTests(QueryTests):
    def test_get_crawls_plotting_data_no_data(self):
        plotting_data = self.mongo_controller.get_crawls_plotting_data(ObjectId())
        self.assertEqual(plotting_data, [], "No plotting data should have been found")

    def test_get_crawls_plotting_data_some_data(self):
        granularity = 60
        offset = 2
        keyword = self.keyword_sample
        crawls = generate_crawls(
            keyword, 10, time_difference=int(granularity / 2) + offset
        )
        self.load_crawls(crawls)

        plotting_data = self.mongo_controller.get_crawls_plotting_data(
            keyword._id, granularity_in_minutes=granularity
        )

        self.assertEqual(
            len(plotting_data),
            int(len(crawls) / 2),
            "every second crawl should have been accumulated",
        )

        for data in plotting_data:
            self.assertEqual(
                data["count"], 2, "Two crawls should have been accumulated"
            )
            self.assertEqual(
                data["score"], 1, "They should all average out to a score of 1"
            )

    def test_get_crawls_plotting_stress_test(self):
        granularity = 120
        offset = 2
        keyword = self.keyword_sample
        crawls = generate_crawls(
            keyword, 20000, time_difference=int(granularity / 2) + offset
        )
        self.load_crawls(crawls)

        plotting_data = self.mongo_controller.get_crawls_plotting_data(
            keyword._id, granularity_in_minutes=granularity
        )

        self.assertEqual(
            len(plotting_data),
            int(len(crawls) / 2),
            "every second crawl should have been accumulated",
        )
