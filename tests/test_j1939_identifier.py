import pytest

from j1939.identifier import J1939Identifier


def test_valid_j1939_identifier():
    identifier = J1939Identifier(
        priority=3,
        pgn=0xF004,
        source_address=0x00,
    )

    assert identifier.priority == 3
    assert identifier.pgn == 0xF004
    assert identifier.source_address == 0x00


def test_priority_must_be_between_0_and_7():
    with pytest.raises(
        ValueError,
        match="J1939 priority must be between 0 and 7",
    ):
        J1939Identifier(priority=8, pgn=0, source_address=0)


def test_pgn_must_fit_18_bits():
    with pytest.raises(
        ValueError,
        match="J1939 PGN must be a 18-bit value",
    ):
        J1939Identifier(priority=0, pgn=0x40000, source_address=0)


def test_source_address_must_be_between_0_and_255():
    with pytest.raises(
        ValueError,
        match="J1939 source address must be between 0 and 255",
    ):
        J1939Identifier(priority=0, pgn=0, source_address=256)


def test_arbitration_id_round_trip():
    original_id = 0x0CF00400

    identifier = J1939Identifier.from_arbitration_id(original_id)

    assert identifier.priority == 3
    assert identifier.pgn == 0xF004
    assert identifier.source_address == 0x00
    assert identifier.to_arbitration_id() == original_id


def test_invalid_j1939_arbitration_id():
    with pytest.raises(
        ValueError,
        match="Invalid J1939 arbitration ID",
    ):
        J1939Identifier.from_arbitration_id(0x20000000)
