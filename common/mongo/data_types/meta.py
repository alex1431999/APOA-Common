class Meta:
    """
    This class holds meta data regarding the project
    """

    # A list of ids with keywords which are publicly accessible
    keywords_public_ids: list

    def __init__(self, keywords_public_ids: list):
        self.keywords_public_ids = keywords_public_ids

    @staticmethod
    def from_dict(dict_input: dict):
        """
        Convert a mongo dict to a keywords object
        """
        return Meta(dict_input["keywords_public_ids"])
