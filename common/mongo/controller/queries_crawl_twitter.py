"""
All twitter crawl result database functionality is defined in this module
"""

from common.mongo.data_types.crawling.crawl_results.twitter_result import TwitterResult

def add_crawl_twitter(self, keyword_id, tweet_id, text, likes, retweets, timestamp):
    """
    Add a new twitter crawl to the crawl twitter collection
    If the tweet already exists, update the document

    :param ObjectId keyword_id: The id of the target keyword used
    :param long tweet_id: The id of the tweet provided by twitter
    :param str text: The tweet text
    :param int likes: The amount of likes the tweet has received
    :param int retweets: The amount of retweets the tweet has received
    :param date timestamp: The time the tweet was created
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
    }

    query = { 'tweet_id': tweet_id }

    return self.crawls_twitter_collection.replace_one(query, document, upsert=True)


def get_crawl_twitter_by_id(self, tweet_id):
    """
    Find a twitter result using the tweet id

    :param long tweet_id: The id assigned to the tweet by twitter
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
                'language': '$keyword.language'
            }
        }
    ]

    try:
        tweet_dict = self.crawls_twitter_collection.aggregate(pipeline).next()
        return TwitterResult.mongo_result_to_twitter_result(tweet_dict)
    except: # The tweet was probably not found
        return None
