"""
All twitter crawl result database functionality is defined in this module
"""
from bson import ObjectId
from datetime import datetime
from pymongo.results import UpdateResult

from common.mongo.data_types.crawling.crawl_results.twitter_result import TwitterResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes
from common.mongo.decorators.validation import validate_id


@validate_id("keyword_id")
def add_crawl_twitter(
    self,
    keyword_id: ObjectId,
    tweet_id: int,
    text: str,
    likes: int,
    retweets: int,
    timestamp: str,
    return_object=False,
    cast=False,
) -> UpdateResult:
    """
    Add a new twitter crawl to the crawl twitter collection
    If the tweet already exists, update the document
    """
    document = {
        "keyword_ref": keyword_id
        if type(keyword_id) is ObjectId
        else ObjectId(keyword_id),
        "tweet_id": tweet_id,
        "text": text,
        "likes": likes,
        "retweets": retweets,
        "timestamp": str(timestamp),
        "crawl_type": CrawlTypes.TWITTER.value,
        "entities": [],
        "categories": [],
    }

    query = {"tweet_id": tweet_id}

    update_result = self.crawls_collection.replace_one(query, document, upsert=True)

    if return_object:
        return self.get_crawl_twitter_by_id(tweet_id, cast)

    return update_result


def get_crawl_twitter_by_id(self, tweet_id: int, cast=False):
    """
    Find a twitter result using the tweet id
    """
    pipeline = [
        {"$match": {"tweet_id": tweet_id}},
        {"$limit": 1},
        {
            "$lookup": {
                "from": self.keywords_collection.name,
                "localField": "keyword_ref",
                "foreignField": "_id",
                "as": "keyword",
            }
        },
        {  # Convert keyword from array to object
            "$project": {
                "_id": 1,
                "tweet_id": 1,
                "text": 1,
                "likes": 1,
                "retweets": 1,
                "timestamp": 1,
                "keyword": {"$arrayElemAt": ["$keyword", 0]},
                "keyword_ref": 1,
                "score": 1,
                "entities": 1,
                "categories": 1,
            }
        },
        {  # Final projection
            "$project": {
                "_id": 1,
                "tweet_id": 1,
                "text": 1,
                "likes": 1,
                "retweets": 1,
                "timestamp": 1,
                "keyword_string": "$keyword.keyword_string",
                "language": "$keyword.language",
                "keyword_ref": 1,
                "score": 1,
                "entities": 1,
                "categories": 1,
            }
        },
    ]

    try:
        tweet = self.crawls_collection.aggregate(pipeline).next()

        if cast:
            tweet = TwitterResult.from_dict(tweet)

        return tweet
    except Exception as ex:  # The tweet was probably not found
        return None
