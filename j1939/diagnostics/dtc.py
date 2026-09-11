from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Dtc:
    """A decoded J1939 diagnostic trouble code."""

    spn: int
    fmi: int
    occurrence_count: int = 0
    source_address: int | None = None
    active: bool = True

    def __post_init__(self) -> None:
        if not 0 <= self.spn <= 0x7FFF:
            raise ValueError("J1939 SPN must be between 0 and 32767")

        if not 0 <= self.fmi <= 0x1F:
            raise ValueError("J1939 FMI must be between 0 and 31")

        if not 0 <= self.occurrence_count <= 0x7F:
            raise ValueError("J1939 occurrence count must be between 0 and 127")

        if self.source_address is not None and not 0 <= self.source_address <= 0xFF:
            raise ValueError("J1939 source address must be between 0 and 255")
