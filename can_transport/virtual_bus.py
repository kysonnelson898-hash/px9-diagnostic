from __future__ import annotations

from collections import deque

from .transport import CanFrame, CanTransport


class VirtualCanBus:
    """In-memory CAN bus shared by multiple virtual transports."""

    def __init__(self) -> None:
        self._queues: list[deque[CanFrame]] = []

    def connect(self) -> "VirtualCanTransport":
        transport = VirtualCanTransport(self)
        self._queues.append(transport._queue)
        return transport

    def broadcast(self, sender: "VirtualCanTransport", frame: CanFrame) -> None:
        for queue in self._queues:
            queue.append(frame)

    def disconnect(self, transport: "VirtualCanTransport") -> None:
        if transport._queue in self._queues:
            self._queues.remove(transport._queue)


class VirtualCanTransport(CanTransport):
    """CAN transport connected to a VirtualCanBus."""

    def __init__(self, bus: VirtualCanBus) -> None:
        self._bus = bus
        self._queue: deque[CanFrame] = deque()
        self._closed = False

    def send(self, frame: CanFrame) -> None:
        if self._closed:
            raise RuntimeError("Transport is closed")

        self._bus.broadcast(self, frame)

    def receive(self, timeout: float | None = None) -> CanFrame | None:
        if self._closed:
            raise RuntimeError("Transport is closed")

        if self._queue:
            return self._queue.popleft()

        return None

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._bus.disconnect(self)
