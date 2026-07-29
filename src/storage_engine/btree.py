from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


class KeyNotFoundException(Exception): pass
class DuplicateKeyException(Exception): pass

class BTreeNode(ABC):
    """
    Composite Component — shared interface for both internal and leaf nodes.
    Allows tree traversal code to be uniform across node types.
    """

    def __init__(self, order: int):
        self.order: int = order
        self.keys: List[Any] = []

    @abstractmethod
    def search(self, key: Any) -> Optional[Any]:
        raise NotImplementedError()

    @abstractmethod
    def insert(self, key: Any, value: Any) -> Optional[Tuple[Any, 'BTreeNode']]:
        """Returns a (split_key, new_right_node) tuple when a split occurs, else None."""
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: Any) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        raise NotImplementedError()

    @property
    def is_full(self) -> bool:
        return len(self.keys) >= self.order - 1

    @property
    def is_underfull(self) -> bool:
        return len(self.keys) < (self.order - 1) // 2


class InternalNode(BTreeNode):
    """Composite — holds separator keys and pointers to child BTreeNodes."""

    def __init__(self, order: int):
        super().__init__(order)
        self.children: List[BTreeNode] = []

    @property
    def is_leaf(self) -> bool:
        return False

    def search(self, key: Any) -> Optional[Any]:
        raise NotImplementedError()

    def insert(self, key: Any, value: Any) -> Optional[Tuple[Any, 'BTreeNode']]:
        raise NotImplementedError()

    def delete(self, key: Any) -> None:
        raise NotImplementedError()


class LeafNode(BTreeNode):
    """Leaf — holds actual key→record-pointer pairs. Linked list for range scans."""

    def __init__(self, order: int):
        super().__init__(order)
        self.values: List[Any] = []     
        self.next_leaf: Optional['LeafNode'] = None

    @property
    def is_leaf(self) -> bool:
        return True

    def search(self, key: Any) -> Optional[Any]:
        raise NotImplementedError()

    def insert(self, key: Any, value: Any) -> Optional[Tuple[Any, 'BTreeNode']]:
        raise NotImplementedError()

    def delete(self, key: Any) -> None:
        raise NotImplementedError()


class BTree:
    """B-Tree data structure. Uses Composite BTreeNode to traverse the tree."""

    def __init__(self, order: int = 4):
        self._order: int = order
        self._root: BTreeNode = LeafNode(order)

    def insert_node(self, key: Any, value: Any) -> None:
        raise NotImplementedError()

    def delete_node(self, key: Any) -> None:
        raise NotImplementedError()

    def search_key(self, key: Any) -> Optional[Any]:
        raise NotImplementedError()

    def split_node(self, node: BTreeNode) -> Tuple[Any, BTreeNode]:
        raise NotImplementedError()

    def merge_node(self, left: BTreeNode, right: BTreeNode) -> None:
        raise NotImplementedError()
