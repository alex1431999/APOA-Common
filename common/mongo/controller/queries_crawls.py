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

    for crawls_collection in self.crawls_collections:
        update_result = crawls_collection.update_one(query, update)

        # Skip the rest of the collections if you found the crawl result
        if update_result.modified_count > 0:
            break
