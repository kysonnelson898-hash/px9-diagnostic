from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Identifier:
    """Decoded fields from a J1939 29-bit CAN identifier."""

    priority: int
    pgn: int
    source_address: int

    def __post_init__(self) -> None:
        if not 0 <= self.priority <= 7:
            raise ValueError("J1939 priority must be between 0 and 7")

        if not 0 <= self.pgn <= 0x3FFFF:
            raise ValueError("J1939 PGN must be a 18-bit value")

        if not 0 <= self.source_address <= 0xFF:
            raise ValueError("J1939 source address must be between 0 and 255")
