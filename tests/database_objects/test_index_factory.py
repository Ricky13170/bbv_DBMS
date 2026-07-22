import pytest
from src.database_objects.index_factory import IndexFactory, BTreeIndex, HashIndex

class TestIndexFactory:
    def test_CreateIndex_BTree_ShouldReturnBTreeIndex(self):
        index = IndexFactory.create_index("BTREE", "idx_id", ["id"])
        assert isinstance(index, BTreeIndex)

    def test_CreateIndex_Hash_ShouldReturnHashIndex(self):
        index = IndexFactory.create_index("HASH", "idx_name", ["name"])
        assert isinstance(index, HashIndex)

    def test_CreateIndex_InvalidType_ShouldThrow(self):
        with pytest.raises(Exception):
            IndexFactory.create_index("INVALID", "idx", ["col"])
