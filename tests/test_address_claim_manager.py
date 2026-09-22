import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_manager import AddressClaimManager


def test_manager_accepts_different_source_address():
    manager = AddressClaimManager(
        claim=J1939AddressClaim(source_address=0x80, name=0x2000)
    )
    other = J1939AddressClaim(source_address=0x81, name=0x1000)

    assert manager.can_use_address(other) is True


def test_manager_uses_name_priority_for_same_source_address():
    manager = AddressClaimManager(
        claim=J1939AddressClaim(source_address=0x80, name=0x1000)
    )
    other = J1939AddressClaim(source_address=0x80, name=0x2000)

    assert manager.can_use_address(other) is True


def test_manager_loses_to_lower_name_for_same_source_address():
    manager = AddressClaimManager(
        claim=J1939AddressClaim(source_address=0x80, name=0x2000)
    )
    other = J1939AddressClaim(source_address=0x80, name=0x1000)

    assert manager.can_use_address(other) is False


def test_manager_rejects_wrong_type():
    manager = AddressClaimManager(
        claim=J1939AddressClaim(source_address=0x80, name=0x1000)
    )

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        manager.can_use_address(object())


def test_manager_replaces_claim():
    original = J1939AddressClaim(source_address=0x80, name=0x1000)
    replacement = J1939AddressClaim(source_address=0x81, name=0x2000)

    manager = AddressClaimManager(claim=original)
    updated = manager.replace_claim(replacement)

    assert updated.claim == replacement
    assert manager.claim == original


def test_manager_rejects_invalid_replacement():
    manager = AddressClaimManager(
        claim=J1939AddressClaim(source_address=0x80, name=0x1000)
    )

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        manager.replace_claim(object())
