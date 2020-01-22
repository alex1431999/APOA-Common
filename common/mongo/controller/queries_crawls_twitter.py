"""
All twitter crawl result database functionality is defined in this module
"""

from common.mongo.data_types.crawling.crawl_results.twitter_result import TwitterResult
from common.mongo.data_types.crawling.enums.crawl_types import CrawlTypes

def add_crawl_twitter(self, keyword_id, tweet_id, text, likes, retweets, timestamp, return_object=False, cast=False):
    """
    Add a new twitter crawl to the crawl twitter collection
    If the tweet already exists, update the document

    :param ObjectId keyword_id: The id of the target keyword used
    :param long tweet_id: The id of the tweet provided by twitter
    :param str text: The tweet text
    :param int likes: The amount of likes the tweet has received
    :param int retweets: The amount of retweets the tweet has received
    :param date timestamp: The time the tweet was created
    :param boolean return_object: If true return the updated object
    :param boolean cast: If true cast the returned object to TwitterResult
    :return: The update result
    :rtype: UpdateResult
    """
    document = {
        'keyword_ref': keyword_id,
        'tweet_id': tweet_id,
        'text': text,
        'likes': likes,
        'retweets': retweets,
        'timestamp': timestamp,
        'crawl_type': CrawlTypes.TWITTER.value,
    }

    query = { 'tweet_id': tweet_id }

    update_result = self.crawls_collection.replace_one(query, document, upsert=True)

    if return_object:
        return self.get_crawl_twitter_by_id(tweet_id, cast)
    
    return update_result

def get_crawl_twitter_by_id(self, tweet_id, cast=False):
    """
    Find a twitter result using the tweet id

    :param long tweet_id: The id assigned to the tweet by twitter
    :param boolean cast: If true cast the returned object to TwitterResult
    :return: The twitter result found
    :rtype: TwitterResult or None
    """
    pipeline = [
        {
            "$match": { 'tweet_id': tweet_id }
        },
        {
            '$limit': 1
        },
        {
            '$lookup': {
                'from': self.keywords_collection.name,
                'localField': 'keyword_ref',
                'foreignField': '_id',
                'as': 'keyword'
            }
        },
        { # Convert keyword from array to object
            '$project': {
                '_id': 1,
                'tweet_id': 1,
                'text': 1,
                'likes': 1,
                'retweets': 1,
                'timestamp': 1,
                'keyword': { '$arrayElemAt': ['$keyword', 0] }
            }
        },
        { # Final projection
            '$project': {
                '_id': 1,
                'tweet_id': 1,
                'text': 1,
                'likes': 1,
                'retweets': 1,
                'timestamp': 1,
                'keyword_string': '$keyword.keyword_string',
                'language': '$keyword.language',
                'keyword_ref': 1,
            }
        }
    ]

    try:
        tweet = self.crawls_collection.aggregate(pipeline).next()
        
        if cast:
            tweet = TwitterResult.from_dict(tweet)
        
        return tweet
    except: # The tweet was probably not found
        return None
