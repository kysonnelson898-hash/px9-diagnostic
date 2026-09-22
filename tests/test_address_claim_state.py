import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_state import AddressClaimState


def test_state_exposes_claim_information():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    state = AddressClaimState(claim=claim)

    assert state.source_address == 0x80
    assert state.name == 0x1000
    assert state.address_valid is True


def test_state_can_be_invalidated():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    state = AddressClaimState(claim=claim)

    invalid = state.invalidate()

    assert invalid.address_valid is False
    assert invalid.claim == claim
    assert state.address_valid is True


def test_state_can_replace_claim():
    original = J1939AddressClaim(source_address=0x80, name=0x1000)
    replacement = J1939AddressClaim(source_address=0x81, name=0x2000)

    state = AddressClaimState(claim=original)
    updated = state.replace_claim(replacement)

    assert updated.claim == replacement
    assert updated.source_address == 0x81
    assert updated.name == 0x2000
    assert updated.address_valid is True


def test_state_rejects_invalid_claim():
    with pytest.raises(TypeError, match="J1939AddressClaim"):
        AddressClaimState(claim=object())


def test_state_rejects_invalid_replacement():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    state = AddressClaimState(claim=claim)

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        state.replace_claim(object())
