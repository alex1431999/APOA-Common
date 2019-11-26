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

def get_unprocessed_crawls(self, limit=sys.maxsize):
    """
    Get all the crawls which don't have a score yet

    :param int limit: The max amount of returned results
    :return: Unprocessed crawls
    :rtype: List<dict>
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
                'text': 1
            }
        }
    ]

    crawls = []
    for crawls_collection in self.crawls_collections:
        crawls += list(crawls_collection.aggregate(pipeline))
        
        if len(crawls) >= limit:
            break
    
    return crawls
