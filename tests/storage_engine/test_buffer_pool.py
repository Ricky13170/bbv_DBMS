import pytest
from unittest.mock import MagicMock

from src.storage_engine.buffer_pool import (
    BufferPool,
    LRUPolicy,
    BufferPoolFullException,
    PageNotPinnedException
)
from src.storage_engine.page_manager import PageManager, PageID
from src.storage_engine.page import Page

class TestLRUPolicy:
    """Strategy Pattern Tests"""

    def setup_method(self):
        self.policy = LRUPolicy()

    def test_select_victim_WhenEmpty_ShouldReturnNone(self):
        assert self.policy.select_victim() is None

    def test_record_access_ShouldTrackMostRecentlyUsed(self):
        page_1 = PageID("data.db", 1)
        page_2 = PageID("data.db", 2)

        self.policy.record_access(page_1)
        self.policy.record_access(page_2)
        
        self.policy.record_access(page_1)
        
        assert self.policy.select_victim() == page_2

    def test_remove_ShouldEvictExactPageId(self):
        page_1 = PageID("data.db", 1)
        self.policy.record_access(page_1)
        
        self.policy.remove(page_1)
        assert self.policy.select_victim() is None


class TestBufferPoolProxy:
    """Proxy Pattern Tests"""
    
    def setup_method(self):
        self.mock_page_manager = MagicMock(spec=PageManager)
        # Mock PageManager.read_page to return a dummy raw byte array
        self.mock_page_manager.read_page.return_value = b"DUMMY_DATA"
        
        self.policy = LRUPolicy()
        self.buffer_pool = BufferPool(
            page_manager=self.mock_page_manager,
            capacity=2,
            eviction_policy=self.policy
        )

    def test_fetch_page_WhenCacheMiss_ShouldCallPageManager_AndCache(self):
        target_page = PageID("data.db", 1)
        
        page = self.buffer_pool.fetch_page(target_page)
        
        # 1. PageManager must be called (Disk I/O)
        self.mock_page_manager.read_page.assert_called_once_with(target_page)
        # 2. Resulting Page object contains the raw bytes
        assert page.get_data() == b"DUMMY_DATA"
        assert page.page_id == target_page

    def test_fetch_page_WhenCacheHit_ShouldProxyFromRAM_AndNotCallPageManager(self):
        target_page = PageID("data.db", 1)
        
        # First Time (Cache Miss)
        self.buffer_pool.fetch_page(target_page)
        self.mock_page_manager.read_page.reset_mock() # Reset call tracking
        
        # Second Time (Cache Hit - magic of Proxy pattern)
        page_hit = self.buffer_pool.fetch_page(target_page)
        
        self.mock_page_manager.read_page.assert_not_called()
        assert page_hit.page_id == target_page

    def test_evict_page_WhenFull_ShouldTriggerEvictionStrategy(self):
        page_1 = PageID("data.db", 1)
        page_2 = PageID("data.db", 2)
        page_3 = PageID("data.db", 3)

        # Fill capacity (capacity = 2)
        self.buffer_pool.fetch_page(page_1)
        self.buffer_pool.fetch_page(page_2)
        
        # Unpin so they can be evicted
        self.buffer_pool.unpin_page(page_1)
        self.buffer_pool.unpin_page(page_2)

        # Fetch 3rd page -> Triggers Eviction via the Strategy
        self.buffer_pool.fetch_page(page_3)
        
        # Page 1 (LRU) should be gone, Page 2 and 3 should be in cache
        # Fetching page 1 again will cause a MISS (calling read_page)
        self.mock_page_manager.read_page.reset_mock()
        self.buffer_pool.fetch_page(page_1)
        self.mock_page_manager.read_page.assert_called_once_with(page_1)

    def test_fetch_page_WhenAllPagesPinned_ShouldRaiseException(self):
        page_1 = PageID("data.db", 1)
        page_2 = PageID("data.db", 2)
        page_3 = PageID("data.db", 3)

        self.buffer_pool.fetch_page(page_1)
        self.buffer_pool.fetch_page(page_2)
        # Pages fetch initially get pinned (pin = 1). Unpin wasn't called.
        
        # Attempt to fetch 3rd page when capacity is 2 and all are pinned => FAIL
        with pytest.raises(BufferPoolFullException):
            self.buffer_pool.fetch_page(page_3)
