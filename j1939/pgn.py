from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Pgn:
    """A validated J1939 Parameter Group Number."""

    value: int

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 0x3FFFF:
            raise ValueError("J1939 PGN must be a 18-bit value")
