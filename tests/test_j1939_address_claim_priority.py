import pytest

from j1939.address_claim import J1939AddressClaim


def test_lower_name_wins_address_claim():
    lower = J1939AddressClaim(
        source_address=0x80,
        name=0x1000,
    )
    higher = J1939AddressClaim(
        source_address=0x80,
        name=0x2000,
    )

    assert lower.wins_address_claim(higher) is True
    assert higher.wins_address_claim(lower) is False


def test_equal_name_does_not_win_against_itself():
    claim = J1939AddressClaim(
        source_address=0x80,
        name=0x1000,
    )

    assert claim.wins_address_claim(claim) is False


def test_wins_address_claim_rejects_wrong_type():
    claim = J1939AddressClaim(
        source_address=0x80,
        name=0x1000,
    )

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        claim.wins_address_claim(object())
