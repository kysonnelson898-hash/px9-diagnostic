import pytest

from can_transport.transport import CanFrame
from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_message import (
    ADDRESS_CLAIM_PGN,
    AddressClaimMessage,
)
from j1939.identifier import J1939Identifier


def test_address_claim_message_round_trip():
    message = AddressClaimMessage(
        claim=J1939AddressClaim(
            source_address=0x80,
            name=0x1122334455667788,
        )
    )

    frame = message.to_can_frame()

    identifier = J1939Identifier.from_arbitration_id(frame.arbitration_id)

    assert identifier.pgn.value == ADDRESS_CLAIM_PGN
    assert identifier.source_address == 0x80
    assert frame.data == bytes.fromhex("8877665544332211")

    decoded = AddressClaimMessage.from_can_frame(frame)

    assert decoded.claim.source_address == 0x80
    assert decoded.claim.name == 0x1122334455667788


def test_address_claim_message_rejects_non_extended_frame():
    frame = CanFrame(
        arbitration_id=0x123,
        data=b"\x00" * 8,
        is_extended_id=False,
    )

    with pytest.raises(ValueError, match="extended"):
        AddressClaimMessage.from_can_frame(frame)


def test_address_claim_message_rejects_wrong_payload_length():
    frame = CanFrame(
        arbitration_id=0x18EEFF80,
        data=b"\x00" * 7,
        is_extended_id=True,
    )

    with pytest.raises(ValueError, match="exactly 8 bytes"):
        AddressClaimMessage.from_can_frame(frame)


def test_address_claim_message_rejects_wrong_pgn():
    identifier = J1939Identifier(
        priority=6,
        pgn=0x00EA00,
        source_address=0x80,
        _destination_address=0xFF,
    )

    frame = CanFrame(
        arbitration_id=identifier.to_arbitration_id(),
        data=b"\x00" * 8,
        is_extended_id=True,
    )

    with pytest.raises(ValueError, match="not a J1939 Address Claim"):
        AddressClaimMessage.from_can_frame(frame)
