from __future__ import annotations

from dataclasses import dataclass

from can_transport.transport import CanFrame
from j1939.identifier import J1939Identifier


@dataclass(frozen=True)
class J1939Frame:
    """A CAN frame interpreted as a J1939 frame."""

    identifier: J1939Identifier
    data: bytes

    @classmethod
    def from_can_frame(cls, frame: CanFrame) -> "J1939Frame":
        """Decode a CAN frame into a J1939 frame."""
        if not frame.is_extended_id:
            raise ValueError("J1939 requires an extended 29-bit CAN identifier")

        identifier = J1939Identifier.from_arbitration_id(
            frame.arbitration_id
        )

        return cls(
            identifier=identifier,
            data=frame.data,
        )
