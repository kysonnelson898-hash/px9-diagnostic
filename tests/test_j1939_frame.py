import pytest

from can_transport.transport import CanFrame
from j1939.frame import J1939Frame


def test_j1939_frame_decodes_extended_can_frame():
    frame = CanFrame(
        arbitration_id=0x0CF00400,
        data=b"\x01\x02\x03\x04",
        is_extended_id=True,
    )

    j1939_frame = J1939Frame.from_can_frame(frame)

    assert j1939_frame.identifier.priority == 3
    assert j1939_frame.identifier.pgn == 0xF004
    assert j1939_frame.identifier.source_address == 0x00
    assert j1939_frame.data == b"\x01\x02\x03\x04"


def test_j1939_frame_rejects_standard_can_frame():
    frame = CanFrame(
        arbitration_id=0x123,
        data=b"\x00",
        is_extended_id=False,
    )

    with pytest.raises(
        ValueError,
        match="J1939 requires an extended 29-bit CAN identifier",
    ):
        J1939Frame.from_can_frame(frame)
