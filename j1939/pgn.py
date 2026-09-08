from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Pgn:
    """A validated J1939 Parameter Group Number."""

    value: int

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 0x3FFFF:
            raise ValueError("J1939 PGN must be a 18-bit value")

    @property
    def data_page(self) -> int:
        """Return the J1939 data-page bit."""
        return (self.value >> 16) & 0x01

    @property
    def pdu_format(self) -> int:
        """Return the 8-bit PDU format field."""
        return (self.value >> 8) & 0xFF

    @property
    def is_pdu1(self) -> bool:
        """Return True when this PGN uses the PDU1 format."""
        return self.pdu_format < 240

    @property
    def is_pdu2(self) -> bool:
        """Return True when this PGN uses the PDU2 format."""
        return self.pdu_format >= 240


    @property
    def has_destination_address(self) -> bool:
        """Return True when this PGN uses a destination address."""
        return self.is_pdu1
