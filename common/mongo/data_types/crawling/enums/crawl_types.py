from enum import Enum

class CrawlTypes(Enum):
    """
    Enumerate all the different types of crawl sources the system supports
    """
    TWITTER = 'Twitter'
    NEWS = 'News'
    NYT = 'New York Times'
