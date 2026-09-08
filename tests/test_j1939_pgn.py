import pytest

from j1939.pgn import J1939Pgn


def test_valid_j1939_pgn():
    pgn = J1939Pgn(value=0xF004)

    assert pgn.value == 0xF004


def test_j1939_pgn_accepts_boundary_values():
    assert J1939Pgn(value=0).value == 0
    assert J1939Pgn(value=0x3FFFF).value == 0x3FFFF


def test_j1939_pgn_rejects_negative_value():
    with pytest.raises(
        ValueError,
        match="J1939 PGN must be a 18-bit value",
    ):
        J1939Pgn(value=-1)


def test_j1939_pgn_rejects_value_above_18_bits():
    with pytest.raises(
        ValueError,
        match="J1939 PGN must be a 18-bit value",
    ):
        J1939Pgn(value=0x40000)
