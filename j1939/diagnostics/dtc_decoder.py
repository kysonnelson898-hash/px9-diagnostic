from __future__ import annotations

from j1939.diagnostics.dtc import J1939Dtc


def decode_dm1_dtc(data: bytes, source_address: int | None = None) -> J1939Dtc:
    """Decode one 4-byte J1939 DM1 DTC entry."""
    if len(data) != 4:
        raise ValueError("A J1939 DM1 DTC entry must contain exactly 4 bytes")

    spn = data[0] | (data[1] << 8) | ((data[2] & 0xE0) << 11)
    fmi = data[2] & 0x1F
    occurrence_count = data[3] & 0x7F

    return J1939Dtc(
        spn=spn,
        fmi=fmi,
        occurrence_count=occurrence_count,
        source_address=source_address,
        active=True,
    )
