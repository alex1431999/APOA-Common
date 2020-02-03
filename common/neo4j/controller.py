"""
This module deals with all Graph database interaction using neo4j
"""
import sys

from neo4j import GraphDatabase

class Neo4jController():
    # The maximum integer Neo4J accepts
    MAX_32_INT = 2147483647

    """
    The Neo4j Controller handles all communication to the Graph Database
    """
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password='root'):
        """
        Initialise the driver

        :param str uri: The URI defining the database that shall be used
        :param str user: The username to access the database
        :param str password: The password to access the database
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def __execute_query(self, query):
        """
        Execture a query onto the driver session

        :param string query: The query to be executed
        """
        return self.session.run(query)

    def add_keyword(self, keyword):
        """
        Add a keyword instance to the Graph Database as a node

        :param Keyword keyword: The keyword that shall be used as node
        """
        query = 'MERGE (kw:Keyword {{ keyword_string: "{}", language: "{}", _id: "{}" }})'.format(keyword.keyword_string, keyword.language, keyword._id)

        self.__execute_query(query)

    def add_entity(self, entity_string, language, score, count, keyword_id):
        """
        Add an entity to a keyword

        :param str entity_string: The string representation of the entity
        :param string language: The langauge of the entity
        :param int score: The sentiment score of the entity
        :param int count: The amount of times an entity was mentioned in relation to the keyword
        :param ObjectId keyword_id: The ID of the keyword which the entity is related to
        """
        # Add node if not exists
        query = 'MERGE (en:Entity {{ entity_string:"{}", language:"{}" }})'.format(entity_string, language)

        self.__execute_query(query)

        # Add relationship if not exists, otherwhise update the relationship
        query = 'MATCH (kw:Keyword), (en:Entity) '
        query += 'WHERE kw.`_id`="{}" AND en.entity_string="{}" AND en.language="{}" '.format(keyword_id, entity_string, language)
        query += 'MERGE (kw)-[mw:mentioned_with]->(en) '.format(count)
        query += 'SET mw.count = CASE WHEN NOT exists(mw.count) THEN 0 ELSE mw.count END '
        query += 'SET mw.score = CASE WHEN NOT exists(mw.score) THEN 0 ELSE mw.score END '
        query += 'SET mw.count = mw.count + {} '.format(count)
        query += 'SET mw.score = mw.score + {} '.format(score)

        self.__execute_query(query)

    def add_category(self, category_string, language, confidence, count, keyword_id):
        """
        Add a category to a keyword

        :param str category_string: The string representation of the category
        :param string language: The langauge of the category
        :param int confidence: The confidence of if the keyword is related to the topic
        :param int count: The amount of times a category was mentioned in relation to the keyword
        :param ObjectId keyword_id: The ID of the keyword which the category is related to
        """
        # Add node if not exists
        query = 'MERGE (ca:Category {{ category_string:"{}", language:"{}" }})'.format(category_string, language)

        self.__execute_query(query)

        # Add relationship if not exists, otherwhise update the relationship
        query = 'MATCH (kw:Keyword), (ca:Category) '
        query += 'WHERE kw.`_id`="{}" AND ca.category_string="{}" AND ca.language="{}" '.format(keyword_id, category_string, language)
        query += 'MERGE (kw)-[mw:mentioned_with]->(ca) '
        query += 'SET mw.count = CASE WHEN NOT exists(mw.count) THEN 0 ELSE mw.count END '
        query += 'SET mw.confidence = CASE WHEN NOT exists(mw.confidence) THEN 0 ELSE mw.confidence END '
        query += 'SET mw.count = mw.count + {} '.format(count)
        query += 'SET mw.confidence = mw.confidence + {}'.format(confidence)

        self.__execute_query(query)


    def get_keyword_entities(self, keyword, entity_limit=Neo4jController.MAX_32_INT):
        """
        Get a keyword with it's entities and categories

        :param Keyword keyword: The target keyword
        :param int entity_limit: The top amount of entities returned
        """
        query = 'MATCH (kw:Keyword)-[mw:mentioned_with]->(en:Entity)'
        query += 'WHERE kw.`_id`="{}" '.format(keyword._id)
        query += 'RETURN kw, en, mw '
        query += 'ORDER BY mw.score DESC '
        query += 'LIMIT {}'.format(entity_limit)

        entities = self.__execute_query(query).records()

        return entities

    def get_keyword_categories(self, keyword, category_limit=Neo4jController.MAX_32_INT):
        """
        Get a keyword's categories

        :param Keyword keyword: The target keyword
        :param int category_limit: The top amount of categories returned
        """
        query = 'MATCH (kw:Keyword)-[mw:mentioned_with]->(ca:Category) '
        query += 'WHERE kw.`_id`="{}" '.format(keyword._id)
        query += 'RETURN kw, ca, mw '
        query += 'ORDER BY mw.confidence DESC '
        query += 'LIMIT {}'.format(category_limit)

        categories = self.__execute_query(query).records()

        return categories
