import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_service import AddressClaimService


def test_service_create_initializes_claim():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)

    service = AddressClaimService.create(claim)

    assert service.state.claim == claim
    assert service.is_address_valid() is True


def test_service_handles_winning_incoming_claim():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)
    incoming = J1939AddressClaim(source_address=0x80, name=0x2000)

    service = AddressClaimService.create(current)

    result = service.handle_claim(incoming)

    assert result.address_valid is True
    assert result.claim == current


def test_service_handles_losing_incoming_claim():
    current = J1939AddressClaim(source_address=0x80, name=0x2000)
    incoming = J1939AddressClaim(source_address=0x80, name=0x1000)

    service = AddressClaimService.create(current)

    result = service.handle_claim(incoming)

    assert result.address_valid is False
    assert service.is_address_valid() is False


def test_service_can_claim_new_address():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)
    replacement = J1939AddressClaim(source_address=0x81, name=0x2000)

    service = AddressClaimService.create(current)

    result = service.claim_new_address(replacement)

    assert result.claim == replacement
    assert result.source_address == 0x81
    assert result.name == 0x2000
    assert result.address_valid is True


def test_service_rejects_invalid_initial_claim():
    with pytest.raises(TypeError, match="J1939AddressClaim"):
        AddressClaimService.create(object())


def test_service_rejects_invalid_incoming_claim():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    service = AddressClaimService.create(claim)

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        service.handle_claim(object())


def test_service_rejects_invalid_new_claim():
    claim = J1939AddressClaim(source_address=0x80, name=0x1000)
    service = AddressClaimService.create(claim)

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        service.claim_new_address(object())
