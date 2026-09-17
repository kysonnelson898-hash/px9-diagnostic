from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Dm1LampStatus:
    """Decoded J1939 DM1 lamp status information."""

    mil_on: bool
    mil_flash_rate: int
    red_stop_lamp_on: bool
    red_stop_lamp_flash_rate: int
    amber_warning_lamp_on: bool
    amber_warning_lamp_flash_rate: int
    protect_lamp_on: bool
    protect_lamp_flash_rate: int

    def __post_init__(self) -> None:
        for value in (
            self.mil_flash_rate,
            self.red_stop_lamp_flash_rate,
            self.amber_warning_lamp_flash_rate,
            self.protect_lamp_flash_rate,
        ):
            if not 0 <= value <= 3:
                raise ValueError("DM1 lamp flash rate must be between 0 and 3")


def decode_dm1_lamp_status(data: bytes) -> Dm1LampStatus:
    """Decode the two-byte J1939 DM1 lamp status field."""
    if len(data) != 2:
        raise ValueError("DM1 lamp status must contain exactly 2 bytes")

    first = data[0]
    second = data[1]

    return Dm1LampStatus(
        mil_on=bool(first & 0x03),
        mil_flash_rate=(first >> 2) & 0x03,
        red_stop_lamp_on=bool(first & 0x10),
        red_stop_lamp_flash_rate=(first >> 5) & 0x03,
        amber_warning_lamp_on=bool(second & 0x03),
        amber_warning_lamp_flash_rate=(second >> 2) & 0x03,
        protect_lamp_on=bool(second & 0x10),
        protect_lamp_flash_rate=(second >> 5) & 0x03,
    )
