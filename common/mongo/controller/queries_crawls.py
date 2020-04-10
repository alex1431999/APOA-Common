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

from datetime import datetime
from bson import ObjectId

from common.mongo.data_types.crawling.crawl_result import CrawlResult
from common.mongo.decorators.validation import validate_id

@validate_id('_id')
def get_crawl_by_id(self, _id, cast=False):
    """
    Find and return a crawl object using its ID

    :param ObjectId _id: The ID of the crawl
    :param boolean cast: If true, cast the crawl dict to a CrawlResult
    """
    pipeline = [
        {
            '$match': {
                '_id': _id,
            }
        },
        {
            '$limit': 1,
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
                '_id': 1,
                'keyword_ref': 1,
                'keyword_string': '$keyword.keyword_string',
                'language': '$keyword.language',
                'text': 1,
                'timestamp': 1,
            }
        }
    ]

    try:
        crawl = self.crawls_collection.aggregate(pipeline).next()
    except:
        crawl = None

    if cast and crawl:
        crawl = CrawlResult.from_dict(crawl)
    
    return crawl

def get_unprocessed_crawls(self, limit=sys.maxsize, cast=False):
    """
    Get all the crawls which don't have a score yet

    :param int limit: The max amount of returned results
    :param boolean cast: If true, cast all results to CrawlResult
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
                '_id': 1,
                'keyword_ref': 1,
                'keyword_string': '$keyword.keyword_string',
                'language': '$keyword.language',
                'text': 1,
                'timestamp': 1,
            }
        }
    ]

    crawls = list(self.crawls_collection.aggregate(pipeline))

    if cast:
        crawls = [CrawlResult.from_dict(crawl) for crawl in crawls]
    
    return crawls

@validate_id('_id')
def set_score_crawl(self, _id, score, return_object=False, cast=False):
    """
    Sets the score of a crawl

    :param ObjectId _id: The id of the crawl
    :param int score: The score to be set
    :param boolean return_object: If true return the updated object
    :param boolean cast: If true cast the returned object to CrawlObject
    """
    query = { '_id': _id }
    update = { '$set': { 'score': score } }

    update_result = self.crawls_collection.update_one(query, update)

    if return_object:
        return self.get_crawl_by_id(_id, cast=cast)

    return update_result

@validate_id('keyword_id')
def get_crawls_plotting_data(self, keyword_id, date_cutoff=None):
    """
    Gather all the crawls belonging to the given keyword id
    and transform the data such that it can be used to plot a graph
    using the score.

    You could be more efficient by implementing the Accumulation of the scores piecewise
    in the mongo query. This seems to be quite the challenge and the for loop is just of O(N).
    Still an improvement worth making if this function slows down the process.

    :param ObjectId keyword_id: The id of the target keyword
    :param datetime date_cutoff: Only return plotting data up to that point in time
    """
    # Default date cutoff if none is provided
    if not date_cutoff:
        date_cutoff = datetime(1970,1,1)
    
    pipeline = [
        {
            '$match': {
                'keyword_ref': keyword_id,
                'score': { '$exists': True },
                'timestamp': { '$gte': date_cutoff.isoformat() },
            },
        },
        {
            '$project': {
                '_id': 0,
                'timestamp': 1,
                'score': 1,
                'text': 1,
            },
        },
        {
            '$sort': { 'timestamp': 1 },
        },
    ]

    plotting_data = list(self.crawls_collection.aggregate(pipeline))

    return plotting_data

@validate_id('keyword_id')
def get_crawls_average_score(self, keyword_id):
    pipeline = [
        {
            '$match': { 'keyword_ref': keyword_id },
        },
        {
            '$group': {
                '_id': '$keyword_ref',
                'avg': { '$avg': '$score' }
            }
        }
    ]

    try:
        result = self.crawls_collection.aggregate(pipeline).next()
        avg = result['avg']
    except:
        avg = None

    return avg
