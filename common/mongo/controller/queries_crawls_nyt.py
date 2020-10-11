"""
All nyt crawl result database functionality is defined in this module
"""
from bson import ObjectId

from common.mongo.data_types.crawling.crawl_results.nyt_result import NytResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


def add_crawl_nyt(
    self,
    keyword_id: ObjectId,
    article_id: str,
    text: str,
    timestamp: str,
    return_object=False,
    cast=False,
):
    """
    Add a new nyt article to the crawl collection
    """
    document = {
        "keyword_ref": keyword_id
        if type(keyword_id) is ObjectId
        else ObjectId(keyword_id),
        "article_id": article_id,
        "text": text,
        "timestamp": str(timestamp),
        "crawl_type": CrawlTypes.NYT.value,
        "entities": [],
        "categories": [],
    }

    query = {"article_id": article_id}

    update_result = self.crawls_collection.replace_one(query, document, upsert=True)

    if return_object:
        return self.get_crawl_nyt(article_id, cast)

    return update_result


def get_crawl_nyt(self, article_id, cast=False):
    """
    Find a news article using the article ID

    :param str article_id: The ID of the article provided by NYT
    :param boolean cast: If true cast the returned object to NytResult
    :return: The nyt result found
    :rtype: NytResult or None
    """
    pipeline = [
        {"$match": {"article_id": article_id}},
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
                "article_id": 1,
                "text": 1,
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
                "article_id": 1,
                "text": 1,
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
        nyt_article = self.crawls_collection.aggregate(pipeline).next()

        if cast:
            nyt_article = NytResult.from_dict(nyt_article)

        return nyt_article
    except Exception as ex:  # The article was probably not found
        return None
