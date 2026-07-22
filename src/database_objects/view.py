class View:
    def __init__(self, name: str, query_definition: str):
        self.name = name
        self.query_definition = query_definition

    def resolve(self, schema) -> str:
        raise NotImplementedError()
