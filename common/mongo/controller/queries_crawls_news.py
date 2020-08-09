"""
All news crawl result database functionality is defined in this module

Primary key used to define a news article is author + title
"""

from bson import ObjectId

from common.mongo.data_types.crawling.crawl_results.news_result import NewsResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes


def add_crawl_news(
    self, keyword_id, author, title, text, timestamp, return_object=False, cast=False
):
    """
    Add a new news article to the crawl collection

    :param ObjectId keyword_id: The ID of the keyword used to find the article
    :param str author: The author who has written the article
    :param str title: The title of the articlerticle
    :param str text: The actual article content
    :param date timestamp: The time the article was published
    :param boolean return_object: If true return the updated object
    :param boolean cast: If true cast the returned object to News
    :return: The update result
    :rtype: UpdateResult
    """
    document = {
        "keyword_ref": keyword_id
        if type(keyword_id) is ObjectId
        else ObjectId(keyword_id),
        "author": author,
        "title": title,
        "text": text,
        "timestamp": timestamp,
        "crawl_type": CrawlTypes.NEWS.value,
        "entities": [],
        "categories": [],
    }

    query = {"author": author, "title": title}

    update_result = self.crawls_collection.replace_one(query, document, upsert=True)

    if return_object:
        return self.get_crawl_news(author, title, cast)

    return update_result


def get_crawl_news(self, author, title, cast=False):
    """
    Find a news article using the author and title

    :param str author: The author who has written the article
    :param str title: The title of the article
    :param boolean cast: If true cast the returned object to TwitterResult
    :return: The twitter result found
    :rtype: TwitterResult or None
    """
    pipeline = [
        {"$match": {"author": author, "title": title}},
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
                "author": 1,
                "title": 1,
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
                "author": 1,
                "title": 1,
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
        news_article = self.crawls_collection.aggregate(pipeline).next()

        if cast:
            news_article = NewsResult.from_dict(news_article)

        return news_article
    except Exception as ex:  # The article was probably not found
        return None
