import pytest

from j1939.address import J1939Address


def test_valid_j1939_source_address():
    address = J1939Address(source_address=0x80)

    assert address.source_address == 0x80


def test_lowest_valid_source_address():
    assert J1939Address(source_address=0).source_address == 0


def test_highest_valid_source_address():
    assert J1939Address(source_address=0xFF).source_address == 0xFF


def test_negative_source_address_is_rejected():
    with pytest.raises(
        ValueError,
        match="J1939 source address must be between 0 and 255",
    ):
        J1939Address(source_address=-1)


def test_source_address_above_255_is_rejected():
    with pytest.raises(
        ValueError,
        match="J1939 source address must be between 0 and 255",
    ):
        J1939Address(source_address=256)
