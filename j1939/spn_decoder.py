from __future__ import annotations

from j1939.spn import J1939Spn


def decode_spn(data: bytes, spn: J1939Spn) -> float:
    """Decode one SPN value from a CAN/J1939 payload."""
    if len(data) > 8:
        raise ValueError("J1939 payload cannot exceed 8 bytes")

    if spn.start_bit + spn.bit_length > len(data) * 8:
        raise ValueError("J1939 SPN does not fit within the provided payload")

    raw_value = int.from_bytes(data, byteorder="little", signed=False)

    mask = (1 << spn.bit_length) - 1
    raw_value = (raw_value >> spn.start_bit) & mask

    return raw_value * spn.resolution + spn.offset
