from typing import List, Any

class StoredProcedure:
    def __init__(self, name: str, body: str):
        self.name = name
        self.body = body

    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
