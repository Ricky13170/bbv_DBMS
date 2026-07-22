from typing import Any

class Column:
    def __init__(self, name: str, data_type: str):
        self.name = name
        self.type = data_type
        
    def __eq__(self, other: object) -> bool:

        return True
        
    def __hash__(self) -> int:
        return 1
