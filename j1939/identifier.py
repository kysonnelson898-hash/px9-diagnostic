from __future__ import annotations

from dataclasses import dataclass

from j1939.pgn import J1939Pgn


@dataclass(frozen=True)
class J1939Identifier:
    """Decoded fields from a J1939 29-bit CAN identifier."""

    priority: int
    pgn: J1939Pgn | int
    source_address: int

    def __post_init__(self) -> None:
        if not 0 <= self.priority <= 7:
            raise ValueError("J1939 priority must be between 0 and 7")

        if not 0 <= self.source_address <= 0xFF:
            raise ValueError("J1939 source address must be between 0 and 255")

        if isinstance(self.pgn, int):
            object.__setattr__(self, "pgn", J1939Pgn(self.pgn))
        elif not isinstance(self.pgn, J1939Pgn):
            raise TypeError("J1939 PGN must be an integer or J1939Pgn")

    @classmethod
    def from_arbitration_id(cls, arbitration_id: int) -> "J1939Identifier":
        """Decode a 29-bit CAN arbitration ID into J1939 fields."""
        if not 0 <= arbitration_id <= 0x1FFFFFFF:
            raise ValueError("Invalid J1939 arbitration ID")

        priority = (arbitration_id >> 26) & 0x07
        pgn = J1939Pgn((arbitration_id >> 8) & 0x3FFFF)
        source_address = arbitration_id & 0xFF

        return cls(
            priority=priority,
            pgn=pgn,
            source_address=source_address,
        )

    def to_arbitration_id(self) -> int:
        """Encode this J1939 identifier into a 29-bit CAN arbitration ID."""
        return (
            (self.priority << 26)
            | (self.pgn.value << 8)
            | self.source_address
        )
