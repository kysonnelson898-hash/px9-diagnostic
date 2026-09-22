import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_network import AddressClaimNetwork


def test_register_new_claim():
    network = AddressClaimNetwork()
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    assert network.register(claim) is True
    assert network.get_claim(0x80) == claim
    assert len(network) == 1


def test_lower_name_wins_existing_claim():
    network = AddressClaimNetwork()

    existing = J1939AddressClaim(source_address=0x80, name=0x2000)
    winner = J1939AddressClaim(source_address=0x80, name=0x1000)

    assert network.register(existing) is True
    assert network.register(winner) is True
    assert network.get_claim(0x80) == winner


def test_higher_name_does_not_replace_existing_claim():
    network = AddressClaimNetwork()

    existing = J1939AddressClaim(source_address=0x80, name=0x1000)
    loser = J1939AddressClaim(source_address=0x80, name=0x2000)

    assert network.register(existing) is True
    assert network.register(loser) is False
    assert network.get_claim(0x80) == existing


def test_different_source_addresses_can_coexist():
    network = AddressClaimNetwork()

    first = J1939AddressClaim(source_address=0x80, name=0x1000)
    second = J1939AddressClaim(source_address=0x81, name=0x2000)

    assert network.register(first) is True
    assert network.register(second) is True
    assert len(network) == 2


def test_get_claim_returns_none_when_not_registered():
    network = AddressClaimNetwork()

    assert network.get_claim(0x80) is None


def test_remove_claim():
    network = AddressClaimNetwork()
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    network.register(claim)
    network.remove(0x80)

    assert network.get_claim(0x80) is None
    assert len(network) == 0


def test_remove_missing_claim_is_safe():
    network = AddressClaimNetwork()

    network.remove(0x80)

    assert len(network) == 0


def test_clear_removes_all_claims():
    network = AddressClaimNetwork()

    network.register(J1939AddressClaim(source_address=0x80, name=0x1000))
    network.register(J1939AddressClaim(source_address=0x81, name=0x2000))

    network.clear()

    assert len(network) == 0
    assert network.get_claim(0x80) is None
    assert network.get_claim(0x81) is None


def test_register_rejects_invalid_claim():
    network = AddressClaimNetwork()

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        network.register(object())


@pytest.mark.parametrize("source_address", [-1, 256])
def test_get_claim_rejects_invalid_source_address(source_address):
    network = AddressClaimNetwork()

    with pytest.raises(
        ValueError,
        match="between 0 and 255",
    ):
        network.get_claim(source_address)


@pytest.mark.parametrize("source_address", [-1, 256])
def test_remove_rejects_invalid_source_address(source_address):
    network = AddressClaimNetwork()

    with pytest.raises(
        ValueError,
        match="between 0 and 255",
    ):
        network.remove(source_address)
