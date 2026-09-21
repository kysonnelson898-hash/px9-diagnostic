from __future__ import annotations

from dataclasses import dataclass

from can_transport.transport import CanFrame
from j1939.address_claim import J1939AddressClaim
from j1939.identifier import J1939Identifier


ADDRESS_CLAIM_PGN = 0x00EE00
GLOBAL_DESTINATION = 0xFF


@dataclass(frozen=True)
class AddressClaimMessage:
    """J1939 Address Claim message."""

    claim: J1939AddressClaim

    def to_can_frame(self, priority: int = 6) -> CanFrame:
        """Encode an Address Claim into a J1939 CAN frame."""
        identifier = J1939Identifier(
            priority=priority,
            pgn=ADDRESS_CLAIM_PGN,
            source_address=self.claim.source_address,
            _destination_address=GLOBAL_DESTINATION,
        )

        return CanFrame(
            arbitration_id=identifier.to_arbitration_id(),
            data=self.claim.name_bytes(),
            is_extended_id=True,
        )

    @classmethod
    def from_can_frame(cls, frame: CanFrame) -> "AddressClaimMessage":
        """Decode a J1939 Address Claim CAN frame."""
        if not frame.is_extended_id:
            raise ValueError("Address Claim requires an extended CAN identifier")

        if len(frame.data) != 8:
            raise ValueError("Address Claim payload must contain exactly 8 bytes")

        identifier = J1939Identifier.from_arbitration_id(frame.arbitration_id)

        if identifier.pgn.value != ADDRESS_CLAIM_PGN:
            raise ValueError("CAN frame is not a J1939 Address Claim")

        name = int.from_bytes(frame.data, byteorder="little", signed=False)

        return cls(
            claim=J1939AddressClaim(
                source_address=identifier.source_address,
                name=name,
            )
        )
