class Index:
    def __init__(self, name: str, columns: list):
        self.name = name
        self.columns = columns

class BTreeIndex(Index): pass
class HashIndex(Index): pass

class IndexFactory:
    @staticmethod
    def create_index(index_type: str, name: str, columns: list) -> Index:
        raise NotImplementedError()
