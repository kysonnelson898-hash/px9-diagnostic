import pytest

from j1939.identifier import J1939Identifier
from j1939.request import J1939Request, REQUEST_PGN


def test_j1939_request_encodes_requested_pgn():
    request = J1939Request(
        requested_pgn=0x00F004,
        source_address=0x80,
        destination_address=0x00,
    )

    frame = request.to_can_frame()
    identifier = J1939Identifier.from_arbitration_id(frame.arbitration_id)

    assert identifier.pgn.value == REQUEST_PGN
    assert identifier.source_address == 0x80
    assert identifier.destination_address == 0x00
    assert frame.data == bytes.fromhex("04F000")


def test_j1939_request_rejects_invalid_requested_pgn():
    with pytest.raises(ValueError, match="18-bit"):
        J1939Request(
            requested_pgn=0x40000,
            source_address=0x80,
        )


def test_j1939_request_rejects_invalid_source_address():
    with pytest.raises(ValueError, match="Source address"):
        J1939Request(
            requested_pgn=0x00F004,
            source_address=0x100,
        )


def test_j1939_request_rejects_invalid_destination_address():
    with pytest.raises(ValueError, match="Destination address"):
        J1939Request(
            requested_pgn=0x00F004,
            source_address=0x80,
            destination_address=0x100,
        )


def test_j1939_request_rejects_invalid_priority():
    with pytest.raises(ValueError, match="priority"):
        J1939Request(
            requested_pgn=0x00F004,
            source_address=0x80,
            priority=8,
        )
