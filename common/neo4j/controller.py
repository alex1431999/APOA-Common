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
