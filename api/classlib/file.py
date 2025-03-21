class File:
    """
    Class to help manage files.
    """

    def __init__(self, id: str = None, name: str = None, path: str = None, cksum=None):
        """
        Initialiazation object.

        Args:
            id (str): UUID unique for file indentification.
            name (str): File name.
            path (str): File path.
            cksum (str): checksum of the file to ensure its integrity.
        """
        self.id = id  # Ussing a UUID for the id
        self.name = name
        self.path = path
        self.cksum = cksum

    def __repr__(self):
        """
        Object representation for easy viewing
        """
        return (
            f'file_name: {self.name}, file_id: {self.id}, '
            f'file_path: {self.path}, file_cksum: {self.cksum}'
        )

    @staticmethod
    def fromjson(obj):
        pass
