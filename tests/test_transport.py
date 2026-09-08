from can_transport.transport import CanFrame, CanTransport


class FakeTransport(CanTransport):
    def __init__(self):
        self.sent = []

    def send(self, frame: CanFrame) -> None:
        self.sent.append(frame)

    def receive(self, timeout: float | None = None) -> CanFrame | None:
        return self.sent.pop(0) if self.sent else None

    def close(self) -> None:
        pass


def test_can_frame():
    frame = CanFrame(
        arbitration_id=0x18FF0000,
        data=b"\x01\x02\x03",
    )

    assert frame.arbitration_id == 0x18FF0000
    assert frame.data == b"\x01\x02\x03"
    assert frame.is_extended_id is True


def test_transport_send_and_receive():
    transport = FakeTransport()
    frame = CanFrame(arbitration_id=0x123, data=b"\xAA")

    transport.send(frame)

    assert transport.receive() == frame
    assert transport.receive() is None
