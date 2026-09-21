import pytest

from j1939.pgn_definition import J1939PgnDefinition
from j1939.pgn_registry import J1939PgnRegistry


def test_registry_starts_empty():
    registry = J1939PgnRegistry()

    assert len(registry) == 0


def test_registry_registers_and_retrieves_definition():
    registry = J1939PgnRegistry()
    definition = J1939PgnDefinition(
        pgn=0x00F004,
        name="Electronic Engine Controller 1",
    )

    registry.register(definition)

    assert len(registry) == 1
    assert registry.get(0x00F004) == definition


def test_registry_returns_none_for_unknown_pgn():
    registry = J1939PgnRegistry()

    assert registry.get(0x00F004) is None


def test_registry_rejects_duplicate_pgn():
    registry = J1939PgnRegistry()
    definition = J1939PgnDefinition(
        pgn=0x00F004,
        name="Electronic Engine Controller 1",
    )

    registry.register(definition)

    with pytest.raises(ValueError, match="already registered"):
        registry.register(definition)
