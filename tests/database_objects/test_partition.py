import pytest
from src.database_objects.partition import PartitionStrategy, PartitionRangeOverlapException, PartitionNotFoundException

class TestPartitionStrategy:

    # ── Range Management ─────────────────────────────────────────────────────

    def test_AddRange_WhenRangeIsValid_ShouldAddRange(self):
        strategy = PartitionStrategy("created_at")
        strategy.add_range("q1", "2023-01-01", "2023-03-31")
        assert "q1" in strategy._ranges

    def test_AddRange_WhenRangesOverlap_ShouldThrow(self):
        strategy = PartitionStrategy("created_at")
        strategy.add_range("q1", "2023-01-01", "2023-03-31")
        with pytest.raises(PartitionRangeOverlapException):
            strategy.add_range("q1_overlap", "2023-02-01", "2023-04-30")

    def test_RemoveRange_WhenRangeExists_ShouldRemoveRange(self):
        strategy = PartitionStrategy("created_at")
        strategy.add_range("q1", "2023-01-01", "2023-03-31")
        strategy.remove_range("q1")
        assert "q1" not in strategy._ranges

    def test_RemoveRange_WhenRangeDoesNotExist_ShouldThrow(self):
        strategy = PartitionStrategy("created_at")
        with pytest.raises(PartitionNotFoundException):
            strategy.remove_range("invalid_range")

    # ── Routing ──────────────────────────────────────────────────────────────

    def test_RouteRow_WhenKeyMatchesRange_ShouldReturnPartition(self):
        strategy = PartitionStrategy("id")
        strategy.add_range("p1", 1, 100)
        target = strategy.route_row(50)
        assert target == "p1"

    def test_RouteRow_WhenKeyIsOutsideRange_ShouldFail(self):
        strategy = PartitionStrategy("id")
        strategy.add_range("p1", 1, 100)
        with pytest.raises(PartitionNotFoundException):
            strategy.route_row(500)

    def test_RouteRow_WhenKeyIsOnBoundary_ShouldUseConfiguredBoundary(self):
        strategy = PartitionStrategy("id")
        strategy.add_range("p1", 1, 100)  # say, inclusive end
        strategy.add_range("p2", 101, 200) # exclusive start
        # Green phase test expectation: boundary logic resolves to p1
        target = strategy.route_row(100)
        assert target == "p1"
