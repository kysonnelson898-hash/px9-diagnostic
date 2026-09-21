import pytest

from j1939.pgn_definition import J1939PgnDefinition


def test_pgn_definition_accepts_valid_pgn():
    definition = J1939PgnDefinition(
        pgn=0x00F004,
        name="Electronic Engine Controller 1",
    )

    assert definition.pgn == 0x00F004
    assert definition.name == "Electronic Engine Controller 1"


def test_pgn_definition_allows_empty_name():
    definition = J1939PgnDefinition(pgn=0x00EA00)

    assert definition.pgn == 0x00EA00
    assert definition.name == ""


def test_pgn_definition_rejects_negative_pgn():
    with pytest.raises(ValueError, match="18-bit"):
        J1939PgnDefinition(pgn=-1)


def test_pgn_definition_rejects_pgn_above_18_bits():
    with pytest.raises(ValueError, match="18-bit"):
        J1939PgnDefinition(pgn=0x40000)
