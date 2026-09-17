import pytest

from j1939.diagnostics.dm1 import decode_dm1


def test_decode_dm1_with_one_dtc():
    data = bytes([
        0x01, 0x00,
        0xBE, 0x00, 0x01, 0x02,
    ])

    message = decode_dm1(data, source_address=0)

    assert message.lamp_status == bytes([0x01, 0x00])
    assert len(message.dtcs) == 1
    assert message.dtcs[0].spn == 190
    assert message.dtcs[0].fmi == 1
    assert message.dtcs[0].occurrence_count == 2
    assert message.dtcs[0].source_address == 0


def test_decode_dm1_with_no_dtcs():
    message = decode_dm1(bytes([0x00, 0x00]))

    assert message.lamp_status == bytes([0x00, 0x00])
    assert message.dtcs == ()


def test_decode_dm1_rejects_short_payload():
    with pytest.raises(ValueError, match="at least 2 bytes"):
        decode_dm1(bytes([0x00]))


def test_decode_dm1_rejects_incomplete_dtc():
    with pytest.raises(ValueError, match="complete 4-byte entries"):
        decode_dm1(bytes([0x00, 0x00, 0xBE, 0x00, 0x01]))
