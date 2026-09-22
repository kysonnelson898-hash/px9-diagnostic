from __future__ import annotations

from dataclasses import dataclass, field

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_service import AddressClaimService


@dataclass
class AddressClaimNetwork:
    """Track J1939 address claims from multiple ECUs."""

    claims: dict[int, J1939AddressClaim] = field(default_factory=dict)

    def register(self, claim: J1939AddressClaim) -> bool:
        """Register a claim and return whether it wins the address."""
        if not isinstance(claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

        existing = self.claims.get(claim.source_address)

        if existing is None:
            self.claims[claim.source_address] = claim
            return True

        if claim.wins_address_claim(existing):
            self.claims[claim.source_address] = claim
            return True

        return False

    def get_claim(self, source_address: int) -> J1939AddressClaim | None:
        """Return the current claim for a source address."""
        if not 0 <= source_address <= 0xFF:
            raise ValueError("source_address must be between 0 and 255")

        return self.claims.get(source_address)

    def remove(self, source_address: int) -> None:
        """Remove the current claim for a source address."""
        if not 0 <= source_address <= 0xFF:
            raise ValueError("source_address must be between 0 and 255")

        self.claims.pop(source_address, None)

    def clear(self) -> None:
        """Remove all tracked address claims."""
        self.claims.clear()

    def __len__(self) -> int:
        """Return the number of currently claimed source addresses."""
        return len(self.claims)
