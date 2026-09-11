import pytest

from j1939.diagnostics.dtc_decoder import decode_dm1_dtc


def test_decode_dm1_dtc():
    dtc = decode_dm1_dtc(bytes([0xBE, 0x00, 0x01, 0x02]), source_address=0)

    assert dtc.spn == 190
    assert dtc.fmi == 1
    assert dtc.occurrence_count == 2
    assert dtc.source_address == 0
    assert dtc.active is True


def test_decode_dm1_dtc_rejects_invalid_length():
    with pytest.raises(ValueError, match="exactly 4 bytes"):
        decode_dm1_dtc(bytes([0xBE, 0x00, 0x01]))
