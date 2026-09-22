from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939AddressClaim:
    """J1939 address-claim information for an ECU."""

    source_address: int
    name: int

    def __post_init__(self) -> None:
        if not 0 <= self.source_address <= 0xFF:
            raise ValueError("J1939 source address must be between 0 and 255")

        if not 0 <= self.name <= 0xFFFFFFFFFFFFFFFF:
            raise ValueError("J1939 NAME must be a 64-bit unsigned value")

    def name_bytes(self) -> bytes:
        """Return the 64-bit J1939 NAME in little-endian byte order."""
        return self.name.to_bytes(8, byteorder="little", signed=False)

    def wins_address_claim(self, other: "J1939AddressClaim") -> bool:
        """Return True when this ECU has higher J1939 NAME priority."""
        if not isinstance(other, J1939AddressClaim):
            raise TypeError("other must be a J1939AddressClaim")

        return self.name < other.name
