class Index:
    def __init__(self, name: str, columns: list):
        self.name = name
        self.columns = columns

class BTreeIndex(Index):
    def __init__(self, name: str, columns: list):
        super().__init__(name, columns)

class HashIndex(Index):
    def __init__(self, name: str, columns: list):
        super().__init__(name, columns)

class IndexFactory:
    @staticmethod
    def create_index(index_type: str, name: str, columns: list) -> Index:
        type_upper = index_type.upper()
        if type_upper == "BTREE":
            return BTreeIndex(name, columns)
        elif type_upper == "HASH":
            return HashIndex(name, columns)
        else:
            raise ValueError(f"Unsupported index type: {index_type}")
