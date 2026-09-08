from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CanFrame:
    arbitration_id: int
    data: bytes
    is_extended_id: bool = True

    def __post_init__(self) -> None:
        max_id = 0x1FFFFFFF if self.is_extended_id else 0x7FF

        if not 0 <= self.arbitration_id <= max_id:
            raise ValueError("Invalid CAN arbitration ID")

        if len(self.data) > 8:
            raise ValueError("Classic CAN frame data cannot exceed 8 bytes")


class CanTransport(ABC):
    """Common interface for simulated and real CAN transports."""

    @abstractmethod
    def send(self, frame: CanFrame) -> None:
        """Transmit one CAN frame."""
        raise NotImplementedError

    @abstractmethod
    def receive(self, timeout: float | None = None) -> CanFrame | None:
        """Receive one CAN frame, or None when no frame is available."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Release transport resources."""
        raise NotImplementedError
