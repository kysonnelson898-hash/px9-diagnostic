from can_transport.transport import CanFrame
from can_transport.virtual_bus import VirtualCanBus


def test_virtual_bus_broadcasts_frames():
    bus = VirtualCanBus()
    diagnostic = bus.connect()
    ecm = bus.connect()

    frame = CanFrame(
        arbitration_id=0x18FF0000,
        data=b"\x01\x02\x03\x04",
    )

    diagnostic.send(frame)

    assert diagnostic.receive() == frame
    assert ecm.receive() == frame

    diagnostic.close()
    ecm.close()


def test_closed_transport_cannot_send_or_receive():
    bus = VirtualCanBus()
    transport = bus.connect()

    transport.close()

    try:
        transport.send(CanFrame(arbitration_id=0x123, data=b"\x00"))
        assert False, "send() should fail after close()"
    except RuntimeError as exc:
        assert str(exc) == "Transport is closed"

    try:
        transport.receive()
        assert False, "receive() should fail after close()"
    except RuntimeError as exc:
        assert str(exc) == "Transport is closed"
