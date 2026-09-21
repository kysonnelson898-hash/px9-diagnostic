from __future__ import annotations

from dataclasses import dataclass

from can_transport.transport import CanFrame
from j1939.identifier import J1939Identifier


REQUEST_PGN = 0x00EA00


@dataclass(frozen=True)
class J1939Request:
    """J1939 Request message for a Parameter Group Number."""

    requested_pgn: int
    source_address: int
    destination_address: int = 0xFF
    priority: int = 6

    def __post_init__(self) -> None:
        if not 0 <= self.requested_pgn <= 0x3FFFF:
            raise ValueError("Requested PGN must be an 18-bit value")

        if not 0 <= self.source_address <= 0xFF:
            raise ValueError("Source address must be between 0 and 255")

        if not 0 <= self.destination_address <= 0xFF:
            raise ValueError("Destination address must be between 0 and 255")

        if not 0 <= self.priority <= 7:
            raise ValueError("J1939 priority must be between 0 and 7")

    def to_can_frame(self) -> CanFrame:
        """Encode this request as a J1939 CAN frame."""
        identifier = J1939Identifier(
            priority=self.priority,
            pgn=REQUEST_PGN,
            source_address=self.source_address,
            _destination_address=self.destination_address,
        )

        return CanFrame(
            arbitration_id=identifier.to_arbitration_id(),
            data=self.requested_pgn.to_bytes(3, byteorder="little"),
            is_extended_id=True,
        )

    @classmethod
    def from_can_frame(cls, frame: CanFrame) -> "J1939Request":
        """Decode a J1939 Request CAN frame."""
        if not frame.is_extended_id:
            raise ValueError("J1939 Request requires an extended CAN identifier")

        if len(frame.data) != 3:
            raise ValueError("J1939 Request payload must contain exactly 3 bytes")

        identifier = J1939Identifier.from_arbitration_id(frame.arbitration_id)

        if identifier.pgn.value != REQUEST_PGN:
            raise ValueError("CAN frame is not a J1939 Request")

        if identifier.destination_address is None:
            raise ValueError("J1939 Request requires a destination address")

        requested_pgn = int.from_bytes(
            frame.data,
            byteorder="little",
            signed=False,
        )

        return cls(
            requested_pgn=requested_pgn,
            source_address=identifier.source_address,
            destination_address=identifier.destination_address,
            priority=identifier.priority,
        )
