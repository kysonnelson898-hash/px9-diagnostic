from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class J1939Spn:
    """Definition of a J1939 Suspect Parameter Number."""

    number: int
    start_bit: int
    bit_length: int
    resolution: float = 1.0
    offset: float = 0.0
    units: str = ""

    def __post_init__(self) -> None:
        if not 0 <= self.number <= 0x7FFFF:
            raise ValueError("J1939 SPN number must be between 0 and 524287")

        if self.start_bit < 0:
            raise ValueError("J1939 SPN start bit must be non-negative")

        if self.bit_length <= 0:
            raise ValueError("J1939 SPN bit length must be greater than 0")

        if self.start_bit + self.bit_length > 64:
            raise ValueError("J1939 SPN must fit within a CAN payload")

        if self.resolution <= 0:
            raise ValueError("J1939 SPN resolution must be greater than 0")
