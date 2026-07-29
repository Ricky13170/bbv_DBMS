from enum import Enum

class LockMode(Enum):
    SHARED = "shared"
    EXCLUSIVE = "exclusive"

class LockManager:
    """Mediator — acts as a central authority regulating transaction access to pages."""

    def acquire_lock(self, txn_id: str, page_id: str, mode: LockMode) -> bool:
        raise NotImplementedError()

    def release_lock(self, txn_id: str, page_id: str) -> None:
        raise NotImplementedError()

    def release_all_locks(self, txn_id: str) -> None:
        raise NotImplementedError()
