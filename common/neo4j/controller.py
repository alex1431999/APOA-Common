"""
This module deals with all Graph database interaction using neo4j
"""

from neo4j import GraphDatabase

class Neo4jController():
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

    def __execute_query(self, query):
        """
        Execture a query onto the driver session

        :param string query: The query to be executed
        """
        with self.driver.session() as session:
            session.run(query)

    def add_keyword(self, keyword):
        """
        Add a keyword instance to the Graph Database as a node

        :param Keyword keyword: The keyword that shall be used as node
        """
        query = 'MERGE (kw:Keyword {{ keyword_string: "{}", language: "{}", _id: "{}" }})'.format(keyword.keyword_string, keyword.language, keyword._id)

        self.__execute_query(query)

    def add_entity(self, entity_string, language, count, keyword_id):
        """
        Add an entity to a keyword

        :param str entity_string: The string representation of the entity
        :param string language: The langauge of the entity
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
        query += 'SET mw.count={}'.format(count)

        self.__execute_query(query)

    def add_category(self, category_string, language, count, keyword_id):
        """
        Add a category to a keyword

        :param str category_string: The string representation of the category
        :param string language: The langauge of the category
        :param int count: The amount of times a category was mentioned in relation to the keyword
        :param ObjectId keyword_id: The ID of the keyword which the category is related to
        """
        # Add node if not exists
        query = 'MERGE (ca:category {{ category_string:"{}", language:"{}" }})'.format(category_string, language)

        self.__execute_query(query)

        # Add relationship if not exists, otherwhise update the relationship
        query = 'MATCH (kw:Keyword), (ca:category) '
        query += 'WHERE kw.`_id`="{}" AND ca.category_string="{}" AND ca.language="{}" '.format(keyword_id, category_string, language)
        query += 'MERGE (kw)-[mw:mentioned_with]->(ca) '.format(count)
        query += 'SET mw.count={}'.format(count)

        self.__execute_query(query)
