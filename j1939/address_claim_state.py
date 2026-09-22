from __future__ import annotations

from dataclasses import dataclass

from j1939.address_claim import J1939AddressClaim


@dataclass(frozen=True)
class AddressClaimState:
    """Track the current state of a J1939 address claim."""

    claim: J1939AddressClaim
    address_valid: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

    @property
    def source_address(self) -> int:
        """Return the ECU's currently claimed source address."""
        return self.claim.source_address

    @property
    def name(self) -> int:
        """Return the ECU's J1939 NAME."""
        return self.claim.name

    def invalidate(self) -> "AddressClaimState":
        """Return a state representing an invalid address claim."""
        return AddressClaimState(
            claim=self.claim,
            address_valid=False,
        )

    def replace_claim(
        self,
        claim: J1939AddressClaim,
    ) -> "AddressClaimState":
        """Return a new state using a replacement address claim."""
        if not isinstance(claim, J1939AddressClaim):
            raise TypeError("claim must be a J1939AddressClaim")

        return AddressClaimState(
            claim=claim,
            address_valid=True,
        )
