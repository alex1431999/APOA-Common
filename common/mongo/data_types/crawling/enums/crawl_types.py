from enum import Enum


class CrawlTypes(Enum):
    """
    Enumerate all the different types of crawl sources the system supports
    """

    NEUTRAL = "Neutral"  # For creating an instance of the crawl parent class
    TWITTER = "Twitter"
    NEWS = "News"
    NYT = "New York Times"
