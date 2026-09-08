from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Address:
    """A J1939 ECU source address."""

    source_address: int

    def __post_init__(self) -> None:
        if not 0 <= self.source_address <= 0xFF:
            raise ValueError("J1939 source address must be between 0 and 255")
