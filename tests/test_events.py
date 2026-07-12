from sephirothos.events import EventBus


def test_quit_request_can_be_observed() -> None:
    event_bus = EventBus()
    received: list[bool] = []

    event_bus.quit_requested.connect(lambda: received.append(True))
    event_bus.quit_requested.emit()

    assert received == [True]


def test_restart_request_can_be_observed() -> None:
    event_bus = EventBus()
    received: list[bool] = []

    event_bus.restart_requested.connect(lambda: received.append(True))
    event_bus.restart_requested.emit()

    assert received == [True]


def test_notification_contains_message() -> None:
    event_bus = EventBus()
    received: list[str] = []

    event_bus.notification_requested.connect(received.append)
    event_bus.notification_requested.emit("Update available")

    assert received == ["Update available"]
