import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_registry import AddressClaimRegistry


def test_register_new_claim():
    registry = AddressClaimRegistry()
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    assert registry.register(claim) is True
    assert registry.get(0x80) == claim
    assert len(registry) == 1


def test_lower_name_replaces_existing_claim():
    registry = AddressClaimRegistry()

    existing = J1939AddressClaim(source_address=0x80, name=0x2000)
    winner = J1939AddressClaim(source_address=0x80, name=0x1000)

    registry.register(existing)

    assert registry.register(winner) is True
    assert registry.get(0x80) == winner


def test_higher_name_does_not_replace_existing_claim():
    registry = AddressClaimRegistry()

    existing = J1939AddressClaim(source_address=0x80, name=0x1000)
    loser = J1939AddressClaim(source_address=0x80, name=0x2000)

    registry.register(existing)

    assert registry.register(loser) is False
    assert registry.get(0x80) == existing


def test_multiple_addresses_can_be_registered():
    registry = AddressClaimRegistry()

    first = J1939AddressClaim(source_address=0x80, name=0x1000)
    second = J1939AddressClaim(source_address=0x81, name=0x2000)

    assert registry.register(first) is True
    assert registry.register(second) is True
    assert len(registry) == 2


def test_get_missing_claim_returns_none():
    registry = AddressClaimRegistry()

    assert registry.get(0x80) is None


def test_all_claims_returns_registered_claims():
    registry = AddressClaimRegistry()

    first = J1939AddressClaim(source_address=0x80, name=0x1000)
    second = J1939AddressClaim(source_address=0x81, name=0x2000)

    registry.register(first)
    registry.register(second)

    assert set(registry.all_claims()) == {first, second}


def test_remove_claim():
    registry = AddressClaimRegistry()
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    registry.register(claim)
    registry.remove(0x80)

    assert registry.get(0x80) is None
    assert len(registry) == 0


def test_remove_missing_claim_is_safe():
    registry = AddressClaimRegistry()

    registry.remove(0x80)

    assert len(registry) == 0


def test_clear_removes_all_claims():
    registry = AddressClaimRegistry()

    registry.register(
        J1939AddressClaim(source_address=0x80, name=0x1000)
    )
    registry.register(
        J1939AddressClaim(source_address=0x81, name=0x2000)
    )

    registry.clear()

    assert len(registry) == 0
    assert registry.all_claims() == ()


def test_register_rejects_invalid_claim():
    registry = AddressClaimRegistry()

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        registry.register(object())


@pytest.mark.parametrize("source_address", [-1, 256])
def test_get_rejects_invalid_source_address(source_address):
    registry = AddressClaimRegistry()

    with pytest.raises(ValueError, match="between 0 and 255"):
        registry.get(source_address)


@pytest.mark.parametrize("source_address", [-1, 256])
def test_remove_rejects_invalid_source_address(source_address):
    registry = AddressClaimRegistry()

    with pytest.raises(ValueError, match="between 0 and 255"):
        registry.remove(source_address)
