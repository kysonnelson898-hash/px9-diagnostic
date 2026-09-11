import pytest

from j1939.spn import J1939Spn
from j1939.spn_decoder import decode_spn


def test_decode_spn_extracts_value():
    spn = J1939Spn(number=190, start_bit=0, bit_length=16)
    data = bytes([0x34, 0x12])
    assert decode_spn(data, spn) == 0x1234


def test_decode_spn_applies_resolution_and_offset():
    spn = J1939Spn(
        number=100,
        start_bit=0,
        bit_length=8,
        resolution=0.5,
        offset=-10.0,
    )
    data = bytes([40])
    assert decode_spn(data, spn) == 10.0


def test_decode_spn_extracts_nonzero_bit_position():
    spn = J1939Spn(number=101, start_bit=8, bit_length=8)
    data = bytes([0xAA, 0x34])
    assert decode_spn(data, spn) == 0x34


def test_decode_spn_rejects_payload_larger_than_eight_bytes():
    spn = J1939Spn(number=100, start_bit=0, bit_length=8)

    with pytest.raises(ValueError, match="J1939 payload cannot exceed 8 bytes"):
        decode_spn(b"\x00" * 9, spn)


def test_decode_spn_rejects_spn_outside_payload():
    spn = J1939Spn(number=100, start_bit=16, bit_length=8)

    with pytest.raises(
        ValueError,
        match="J1939 SPN does not fit within the provided payload",
    ):
        decode_spn(b"\x00", spn)
