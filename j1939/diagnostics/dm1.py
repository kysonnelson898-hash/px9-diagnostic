cd ~/px9-diagnostic && cat > j1939/diagnostics/dm1.py <<'PY'
from __future__ import annotations

from dataclasses import dataclass

from j1939.diagnostics.dtc_decoder import decode_dm1_dtc


@dataclass(frozen=True)
class Dm1Message:
    """Decoded J1939 DM1 diagnostic message."""

    lamp_status: int
    dtcs: tuple

    def __post_init__(self) -> None:
        if not 0 <= self.lamp_status <= 0xFF:
            raise ValueError("DM1 lamp status must be between 0 and 255")


def decode_dm1(data: bytes, source_address: int | None = None) -> Dm1Message:
    """Decode a J1939 DM1 payload containing lamp status and DTC entries."""
    if len(data) < 2:
        raise ValueError("A J1939 DM1 message must contain at least 2 bytes")

    dtc_data = data[2:]

    if len(dtc_data) % 4 != 0:
        raise ValueError("DM1 DTC data must contain complete 4-byte entries")

    dtcs = tuple(
        decode_dm1_dtc(dtc_data[index:index + 4], source_address)
        for index in range(0, len(dtc_data), 4)
    )

    return Dm1Message(
        lamp_status=data[0],
        dtcs=dtcs,
    )
PY
