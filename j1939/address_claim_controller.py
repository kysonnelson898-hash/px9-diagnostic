from __future__ import annotations

from dataclasses import dataclass

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_state import AddressClaimState


@dataclass
class AddressClaimController:
    """Manage the current J1939 address-claim state for an ECU."""

    state: AddressClaimState

    def process_claim(
        self,
        incoming_claim: J1939AddressClaim,
    ) -> AddressClaimState:
        """Process an incoming claim and update local state when necessary."""
        if not isinstance(incoming_claim, J1939AddressClaim):
            raise TypeError("incoming_claim must be a J1939AddressClaim")

        if incoming_claim.source_address != self.state.source_address:
            return self.state

        if self.state.claim.wins_address_claim(incoming_claim):
            return self.state

        self.state = self.state.invalidate()
        return self.state

    def apply_new_claim(
        self,
        new_claim: J1939AddressClaim,
    ) -> AddressClaimState:
        """Replace the current claim with a new claim."""
        if not isinstance(new_claim, J1939AddressClaim):
            raise TypeError("new_claim must be a J1939AddressClaim")

        self.state = self.state.replace_claim(new_claim)
        return self.state

    def is_address_valid(self) -> bool:
        """Return whether the current address claim is valid."""
        return self.state.address_valid
