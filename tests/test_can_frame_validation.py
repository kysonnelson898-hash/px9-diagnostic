import pytest

from can_transport.transport import CanFrame


def test_valid_extended_can_frame():
    frame = CanFrame(
        arbitration_id=0x1FFFFFFF,
        data=b"\x00" * 8,
        is_extended_id=True,
    )

    assert frame.arbitration_id == 0x1FFFFFFF
    assert len(frame.data) == 8


def test_invalid_extended_can_id():
    with pytest.raises(ValueError, match="Invalid CAN arbitration ID"):
        CanFrame(
            arbitration_id=0x20000000,
            data=b"",
            is_extended_id=True,
        )


def test_valid_standard_can_frame():
    frame = CanFrame(
        arbitration_id=0x7FF,
        data=b"\x01",
        is_extended_id=False,
    )

    assert frame.arbitration_id == 0x7FF


def test_invalid_standard_can_id():
    with pytest.raises(ValueError, match="Invalid CAN arbitration ID"):
        CanFrame(
            arbitration_id=0x800,
            data=b"",
            is_extended_id=False,
        )


def test_can_frame_rejects_more_than_8_data_bytes():
    with pytest.raises(
        ValueError,
        match="Classic CAN frame data cannot exceed 8 bytes",
    ):
        CanFrame(
            arbitration_id=0x123,
            data=b"\x00" * 9,
        )
