from __future__ import annotations

from dataclasses import dataclass

from j1939.address_claim import J1939AddressClaim
from j1939.address_claim_controller import AddressClaimController
from j1939.address_claim_state import AddressClaimState


@dataclass
class AddressClaimService:
    """High-level service for managing an ECU's J1939 address claim."""

    controller: AddressClaimController

    @classmethod
    def create(cls, claim: J1939AddressClaim) -> "AddressClaimService":
        """Create a service with an initial address claim."""
        if not isinstance(claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

        return cls(
            controller=AddressClaimController(
                state=AddressClaimState(claim=claim)
            )
        )

    @property
    def state(self) -> AddressClaimState:
        """Return the current address-claim state."""
        return self.controller.state

    def handle_claim(
        self,
        incoming_claim: J1939AddressClaim,
    ) -> AddressClaimState:
        """Process an incoming J1939 address claim."""
        return self.controller.process_claim(incoming_claim)

    def claim_new_address(
        self,
        new_claim: J1939AddressClaim,
    ) -> AddressClaimState:
        """Apply a new local address claim."""
        return self.controller.apply_new_claim(new_claim)

    def is_address_valid(self) -> bool:
        """Return whether the current local address is valid."""
        return self.controller.is_address_valid()
