import pytest

from j1939.address_claim import J1939AddressClaim


def test_address_claim_accepts_valid_values():
    claim = J1939AddressClaim(
        source_address=0x80,
        name=0x1122334455667788,
    )

    assert claim.source_address == 0x80
    assert claim.name_bytes() == bytes.fromhex("8877665544332211")


def test_address_claim_rejects_invalid_source_address():
    with pytest.raises(ValueError, match="source address"):
        J1939AddressClaim(
            source_address=0x100,
            name=0,
        )


def test_address_claim_rejects_invalid_name():
    with pytest.raises(ValueError, match="64-bit"):
        J1939AddressClaim(
            source_address=0,
            name=0x10000000000000000,
        )
