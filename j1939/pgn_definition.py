from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939PgnDefinition:
    """Basic metadata for a J1939 Parameter Group Number."""

    pgn: int
    name: str = ""

    def __post_init__(self) -> None:
        if not 0 <= self.pgn <= 0x3FFFF:
            raise ValueError("J1939 PGN must be an 18-bit value")
