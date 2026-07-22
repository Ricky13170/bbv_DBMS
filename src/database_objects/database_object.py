from abc import ABC, abstractmethod

class DatabaseObject(ABC):
    """
    Component Interface for the Composite Pattern.
    Both Leaf nodes (Table, View...) and Composite nodes (Schema) 
    implement this interface for unified object management.
    """
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create(self) -> None:
        """Executes creation logic for the object."""
        pass

    @abstractmethod
    def drop(self) -> None:
        """Executes drop logic and cleanup."""
        pass
