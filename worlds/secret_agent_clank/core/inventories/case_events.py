"""Shared tracker for CaseStructure locations that each have a completion bit."""
from typing import TYPE_CHECKING

from ...constants.types import CaseStructure

if TYPE_CHECKING:
    from ...pypine import Pine


def read_flag(pine: "Pine", entry: CaseStructure) -> bool:
    """Read an entry's completion bit; an unconfirmed entry (address 0) always reads as incomplete."""
    if not entry.event_address:
        return False
    return entry.check_flag(pine.read_int8(entry.event_address))


class CaseEventInventory:

    def __init__(self, pine: "Pine", entries: tuple[CaseStructure, ...]) -> None:
        self.pine = pine
        self.entries = entries
        self.completed: dict[str, bool] = dict.fromkeys((str(entry) for entry in entries), False)

    def get(self, entry: CaseStructure) -> bool:
        return read_flag(self.pine, entry)

    def sync(self) -> None:
        """Baseline read without reporting anything as newly completed."""
        self.completed = {str(entry): self.get(entry) for entry in self.entries}

    def sync_from_ap(self, checked_location_names: set[str]) -> None:
        for entry in self.entries:
            name = str(entry)
            if name in checked_location_names:
                self.completed[name] = True

    def check(self) -> list[str]:
        """Location names that are complete but not yet confirmed, so rejected sends are retried."""
        newly: list[str] = []
        for entry in self.entries:
            name = str(entry)
            now = self.get(entry)
            if now:
                if not self.completed.get(name, False):
                    newly.append(name)
            else:
                self.completed[name] = False
        return newly

    def confirm(self, name: str) -> None:
        """Stop reporting `name`; call only once AP has accepted the check."""
        self.completed[name] = True

    def __repr__(self) -> str:
        seen = sum(self.completed.values())
        return f"{type(self).__name__}(completed={seen}/{len(self.entries)})"
