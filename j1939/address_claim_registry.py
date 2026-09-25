from __future__ import annotations

from dataclasses import dataclass, field

from j1939.address_claim import J1939AddressClaim


@dataclass
class AddressClaimRegistry:
    """Registry of currently known J1939 ECU address claims."""

    _claims: dict[int, J1939AddressClaim] = field(default_factory=dict)

    def register(self, claim: J1939AddressClaim) -> bool:
        """Register a claim if it wins the current address claim."""
        if not isinstance(claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

        existing = self._claims.get(claim.source_address)

        if existing is None or claim.wins_address_claim(existing):
            self._claims[claim.source_address] = claim
            return True

        return False

    def get(self, source_address: int) -> J1939AddressClaim | None:
        """Return the claim currently registered for an address."""
        if not 0 <= source_address <= 0xFF:
            raise ValueError("source_address must be between 0 and 255")

        return self._claims.get(source_address)

    def remove(self, source_address: int) -> None:
        """Remove the claim registered for an address."""
        if not 0 <= source_address <= 0xFF:
            raise ValueError("source_address must be between 0 and 255")

        self._claims.pop(source_address, None)

    def clear(self) -> None:
        """Remove all registered claims."""
        self._claims.clear()

    def all_claims(self) -> tuple[J1939AddressClaim, ...]:
        """Return all registered claims."""
        return tuple(self._claims.values())

    def __len__(self) -> int:
        """Return the number of registered source addresses."""
        return len(self._claims)
