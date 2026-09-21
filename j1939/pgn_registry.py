from __future__ import annotations

from j1939.pgn_definition import J1939PgnDefinition


class J1939PgnRegistry:
    """Registry of verified J1939 PGN definitions."""

    def __init__(self) -> None:
        self._definitions: dict[int, J1939PgnDefinition] = {}

    def register(self, definition: J1939PgnDefinition) -> None:
        if definition.pgn in self._definitions:
            raise ValueError(f"PGN 0x{definition.pgn:05X} is already registered")

        self._definitions[definition.pgn] = definition

    def get(self, pgn: int) -> J1939PgnDefinition | None:
        return self._definitions.get(pgn)

    def __len__(self) -> int:
        return len(self._definitions)
