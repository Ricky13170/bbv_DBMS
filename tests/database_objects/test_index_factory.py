import pytest
from src.database_objects.index_factory import IndexFactory, Index, BTreeIndex, HashIndex


class TestIndexFactory:

    def test_CreateIndex_BTree_ShouldReturnBTreeIndex(self):
        index = IndexFactory.create_index("BTREE", "idx_id", ["id"])
        assert isinstance(index, BTreeIndex)

    def test_CreateIndex_Hash_ShouldReturnHashIndex(self):
        index = IndexFactory.create_index("HASH", "idx_name", ["name"])
        assert isinstance(index, HashIndex)

    def test_CreateIndex_InvalidType_ShouldRaiseValueError(self):
        with pytest.raises(ValueError):
            IndexFactory.create_index("INVALID", "idx", ["col"])

    def test_CreateIndex_ShouldPreserveMetadata(self):
        index = IndexFactory.create_index("BTREE", "idx_pk", ["id"], is_unique=True)
        assert index.name == "idx_pk"
        assert index.columns == ["id"]
        assert index.is_unique is True


class TestIndex:

    def test_Insert_WhenKeyIsValid_ShouldAddEntry(self):
        index = BTreeIndex("idx", ["id"])
        index.insert(1, "ptr_001")
        assert index.search(1) is not None

    def test_Insert_WhenUniqueKeyAlreadyExists_ShouldThrow(self):
        index = BTreeIndex("idx", ["id"], is_unique=True)
        index.insert(1, "ptr_001")
        with pytest.raises(Exception):
            index.insert(1, "ptr_002")

    def test_Insert_WhenIndexIsNonUnique_ShouldAllowDuplicateKeys(self):
        index = BTreeIndex("idx", ["category"])
        index.insert("books", "ptr_001")
        index.insert("books", "ptr_002")
        result = index.search("books")
        assert result is not None

    def test_Insert_WhenKeyIsNullAndNullsNotAllowed_ShouldThrow(self):
        index = BTreeIndex("idx", ["id"], allows_null=False)
        with pytest.raises(Exception):
            index.insert(None, "ptr_001")


    def test_Search_WhenKeyExists_ShouldReturnRecordPointer(self):
        index = BTreeIndex("idx", ["id"])
        index.insert(42, "ptr_42")
        assert index.search(42) == "ptr_42"

    def test_Search_WhenKeyDoesNotExist_ShouldReturnNone(self):
        index = BTreeIndex("idx", ["id"])
        assert index.search(999) is None


    def test_Delete_WhenKeyExists_ShouldRemoveEntry(self):
        index = BTreeIndex("idx", ["id"])
        index.insert(5, "ptr_005")
        result = index.delete(5)
        assert result is True
        assert index.search(5) is None

    def test_Delete_WhenKeyDoesNotExist_ShouldReturnFalse(self):
        index = BTreeIndex("idx", ["id"])
        assert index.delete(999) is False


    def test_Update_WhenKeyExists_ShouldReplaceRecordPointer(self):
        index = BTreeIndex("idx", ["id"])
        index.insert(10, "ptr_old")
        index.update(10, "ptr_new")
        assert index.search(10) == "ptr_new"


    def test_RangeSearch_WhenKeysMatch_ShouldReturnOrderedEntries(self):
        index = BTreeIndex("idx", ["age"])
        for age in [25, 30, 35, 40]:
            index.insert(age, f"ptr_{age}")
        result = index.range_search(28, 36)
        assert len(result) == 2
