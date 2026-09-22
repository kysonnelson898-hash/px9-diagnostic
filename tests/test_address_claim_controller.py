import pytest

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_controller import AddressClaimController
from j1939.address_claim_state import AddressClaimState


def test_controller_ignores_claim_for_different_source_address():
    current = J1939AddressClaim(source_address=0x80, name=0x2000)
    incoming = J1939AddressClaim(source_address=0x81, name=0x1000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    result = controller.process_claim(incoming)

    assert result == controller.state
    assert result.address_valid is True
    assert result.claim == current


def test_controller_keeps_address_when_local_name_wins():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)
    incoming = J1939AddressClaim(source_address=0x80, name=0x2000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    result = controller.process_claim(incoming)

    assert result.address_valid is True
    assert result.claim == current


def test_controller_invalidates_address_when_local_name_loses():
    current = J1939AddressClaim(source_address=0x80, name=0x2000)
    incoming = J1939AddressClaim(source_address=0x80, name=0x1000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    result = controller.process_claim(incoming)

    assert result.address_valid is False
    assert result.claim == current
    assert controller.is_address_valid() is False


def test_controller_can_apply_new_claim():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)
    replacement = J1939AddressClaim(source_address=0x81, name=0x2000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    result = controller.apply_new_claim(replacement)

    assert result.claim == replacement
    assert result.source_address == 0x81
    assert result.name == 0x2000
    assert result.address_valid is True
    assert controller.is_address_valid() is True


def test_controller_rejects_invalid_incoming_claim():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        controller.process_claim(object())


def test_controller_rejects_invalid_new_claim():
    current = J1939AddressClaim(source_address=0x80, name=0x1000)

    controller = AddressClaimController(
        state=AddressClaimState(claim=current)
    )

    with pytest.raises(TypeError, match="J1939AddressClaim"):
        controller.apply_new_claim(object())
