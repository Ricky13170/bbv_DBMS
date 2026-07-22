import pytest
from src.database_objects.sequence import Sequence

class TestSequence:

    def test_Sequence_Init_ShouldSetState(self):
        seq = Sequence("id_seq", start=10, increment=2)
        assert seq.name == "id_seq"
        assert seq.start == 10
        assert seq.increment == 2
        assert seq._current_value == 10

    def test_Sequence_Create_ShouldInitialize(self):
        seq = Sequence("id_seq")
        seq.create()
            
    def test_Sequence_Drop_ShouldCleanUp(self):
        seq = Sequence("id_seq")
        seq.drop()

    def test_Sequence_NextValue_ShouldAdvanceState(self):
        seq = Sequence("id_seq", start=1, increment=1)
        # Red phase: expecting this to fail until logic is written
        assert seq.next_value() == 1
