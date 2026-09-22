from __future__ import annotations

from dataclasses import dataclass

from j1939.address_claim import J1939AddressClaim


@dataclass(frozen=True)
class AddressClaimManager:
    """Track an ECU's J1939 address claim."""

    claim: J1939AddressClaim

    def can_use_address(self, other: J1939AddressClaim) -> bool:
        """Return True if this claim wins against another claim."""
        if not isinstance(other, J1939AddressClaim):
            raise TypeError("other must be a J1939AddressClaim")

        if self.claim.source_address != other.source_address:
            return True

        return self.claim.wins_address_claim(other)

    def replace_claim(self, new_claim: J1939AddressClaim) -> "AddressClaimManager":
        """Return a new manager using the supplied address claim."""
        if not isinstance(new_claim, J1939AddressClaim):
            raise TypeError("new_claim must be a J1939AddressClaim")

        return AddressClaimManager(claim=new_claim)
