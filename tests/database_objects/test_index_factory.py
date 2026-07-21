import pytest
from src.database_objects.index_factory import IndexFactory, BTreeIndex, HashIndex

class TestIndexFactory:
    def test_CreateIndex_WithBTreeType_ShouldReturnBTreeIndex(self):
        index = IndexFactory.create_index("BTREE", "idx_users_id", ["id"])
        
        # Verify the Factory successfully dispatched to the BTree subclass
        assert isinstance(index, BTreeIndex)
        assert index.name == "idx_users_id"
        assert index.columns == ["id"]

    def test_CreateIndex_WithHashType_ShouldReturnHashIndex(self):
        index = IndexFactory.create_index("HASH", "idx_users_email", ["email"])
        
        # Verify the Factory successfully dispatched to the Hash subclass
        assert isinstance(index, HashIndex)
        assert index.name == "idx_users_email"

    def test_CreateIndex_WithInvalidType_ShouldThrowValueError(self):
        # Verify defensive programming: factory rejects unknown index types
        with pytest.raises(ValueError):
            IndexFactory.create_index("MAGIC_TREE", "xyz", ["col"])
