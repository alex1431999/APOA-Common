"""
This module deals with queries related to all the crawl collections

Whenever you add a new data collection to the database, make sure that
all elements in the collection share the same core attributes required
by the processor to process the data.
Those attributes are:
    - text
    - keyword_string
    - language
"""
import sys

from bson import ObjectId

from common.mongo.data_types.crawling.crawl_result import CrawlResult

def get_unprocessed_crawls(self, limit=sys.maxsize, cast=False):
    """
    Get all the crawls which don't have a score yet

    :param int limit: The max amount of returned results
    :param bool cast: If true, cast all results to CrawlResult
    :return: Unprocessed crawls
    :rtype: List<CrawlResult> or List<dict>
    """
    pipeline = [
        {
            '$match': { 
                'score': { '$exists': False } 
            }
        },
        {
            '$limit': limit
        },
        {
            '$lookup':
                {
                    'from': self.keywords_collection.name,
                    'localField': 'keyword_ref',
                    'foreignField': '_id',
                    'as': 'keyword', 
                }
        },
        {
            '$unwind': '$keyword'
        },
        {
            '$project': {
                'keyword_string': '$keyword.keyword_string',
                'language': '$keyword.language',
                'text': 1,
                'timestamp': 1,
            }
        }
    ]

    crawls = list(self.crawls_collection.aggregate(pipeline))

    if cast:
        crawls = [CrawlResult.mongo_result_to_crawl_result(crawl) for crawl in crawls]
    
    return crawls

def set_score_crawl(self, _id, score):
    """
    Looks through each crawl collection for the crawl and sets the score

    You could be more efficient by defining what type of crawl you are manipulating
    and already pointing towards the right collection (skipping all other collections)
    which can be implemented if performance ever becomes an issue here.

    :param ObjectId _id: The id of the crawl
    :param int score: The score to be set
    """
    if _id is not ObjectId:
        _id = ObjectId(_id)

    query = { '_id': _id }
    update = { '$set': { 'score': score } }

    update_result = self.crawls_collection.update_one(query, update)

    return update_result
