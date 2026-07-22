import pytest
from unittest.mock import MagicMock
from src.database_objects.constraint import (
    Constraint, ConstraintContext,
    CheckConstraint, UniqueConstraint, PrimaryKeyConstraint,
    ForeignKeyConstraint, ConstraintViolationException,
    IReferentialAction, CascadeAction, RestrictAction, SetNullAction
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def _make_context(row=None, table=None, schema=None, existing_row=None):
    return ConstraintContext(
        candidate_row=row or MagicMock(),
        table=table or MagicMock(),
        schema=schema or MagicMock(),
        existing_row=existing_row,
    )


# ─── ConstraintContext (Value Object) ───────────────────────────────────────

class TestConstraintContext:
    def test_Context_ShouldStoreAllFields(self):
        row = MagicMock()
        table = MagicMock()
        schema = MagicMock()
        ctx = ConstraintContext(row, table, schema)

        assert ctx.candidate_row is row
        assert ctx.table is table
        assert ctx.schema is schema
        assert ctx.existing_row is None

    def test_Context_WithExistingRow_ShouldStoreIt(self):
        existing = MagicMock()
        ctx = _make_context(existing_row=existing)
        assert ctx.existing_row is existing


# ─── Abstract Constraint (enable / disable) ─────────────────────────────────

class TestConstraintBase:
    def test_Constraint_IsEnabledByDefault(self):
        c = CheckConstraint("chk_age", predicate=lambda row: True)
        assert c.is_enabled is True

    def test_Disable_ShouldSkipValidation(self):
        c = CheckConstraint("chk_age", predicate=lambda row: False)
        c.disable()
        result = c.validate(_make_context())
        assert result is True  # disabled — always passes

    def test_Enable_ShouldReactivateValidation(self):
        c = CheckConstraint("chk_age", predicate=lambda row: True)
        c.disable()
        c.enable()
        assert c.is_enabled is True


# ─── CheckConstraint ─────────────────────────────────────────────────────────

class TestCheckConstraint:
    def test_Check_WhenPredicatePasses_ShouldReturnTrue(self):
        c = CheckConstraint("chk_positive_age", predicate=lambda row: True)
        result = c.validate(_make_context())
        assert result is True

    def test_Check_WhenPredicateFails_ShouldThrow(self):
        c = CheckConstraint("chk_positive_age", predicate=lambda row: False)
        with pytest.raises(ConstraintViolationException):
            c.validate(_make_context())


# ─── UniqueConstraint ────────────────────────────────────────────────────────

class TestUniqueConstraint:
    def test_Unique_WhenValueIsNew_ShouldPass(self):
        c = UniqueConstraint("uq_email", column_names=["email"])
        result = c.validate(_make_context())
        assert result is True

    def test_Unique_WhenDuplicateFound_ShouldThrow(self):
        c = UniqueConstraint("uq_email", column_names=["email"])
        existing = MagicMock()
        with pytest.raises(ConstraintViolationException):
            c.validate(_make_context(existing_row=existing))


# ─── PrimaryKeyConstraint ────────────────────────────────────────────────────

class TestPrimaryKeyConstraint:
    def test_PK_WhenValueIsUniqueAndNotNull_ShouldPass(self):
        c = PrimaryKeyConstraint("pk_id", column_names=["id"])
        result = c.validate(_make_context())
        assert result is True

    def test_PK_WhenDuplicateFound_ShouldThrow(self):
        c = PrimaryKeyConstraint("pk_id", column_names=["id"])
        existing = MagicMock()
        with pytest.raises(ConstraintViolationException):
            c.validate(_make_context(existing_row=existing))


# ─── ForeignKeyConstraint ────────────────────────────────────────────────────

class TestForeignKeyConstraint:
    def _make_fk(self, on_delete=None, on_update=None):
        return ForeignKeyConstraint(
            name="fk_user_id",
            child_column_name="user_id",
            referenced_table_name="users",
            referenced_column_name="id",
            on_delete=on_delete or RestrictAction(),
            on_update=on_update or RestrictAction(),
        )

    def test_FK_WhenReferencedRowExists_ShouldPass(self):
        c = self._make_fk()
        result = c.validate(_make_context())
        assert result is True

    def test_FK_WhenReferencedRowMissing_ShouldThrow(self):
        c = self._make_fk()
        with pytest.raises(ConstraintViolationException):
            c.validate(_make_context())


# ─── IReferentialAction (Strategy: Cascade / Restrict / SetNull) ─────────────

class TestReferentialActions:
    def test_CascadeAction_ShouldDeleteChildRows(self):
        action = CascadeAction()
        parent_row = MagicMock()
        child_table = MagicMock()
        action.execute(parent_row, child_table)
        # Green Phase: verify child_table.delete_row was called

    def test_RestrictAction_WhenChildExists_ShouldThrow(self):
        action = RestrictAction()
        parent_row = MagicMock()
        child_table = MagicMock()
        with pytest.raises(ConstraintViolationException):
            action.execute(parent_row, child_table)

    def test_SetNullAction_ShouldNullifyChildColumn(self):
        action = SetNullAction()
        parent_row = MagicMock()
        child_table = MagicMock()
        action.execute(parent_row, child_table)
        # Green Phase: verify FK column set to None
