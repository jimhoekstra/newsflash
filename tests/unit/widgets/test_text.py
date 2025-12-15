from newsflash.widgets.text import Notifications


def test_notifications_push():
    notifications_widget = Notifications()

    # Push a notification
    notifications_widget.push("Test notification", level="info", duration=3000)

    # Check if the notification was added
    assert len(notifications_widget.notifications) == 1
    assert notifications_widget.notifications[0].message == "Test notification"
    assert notifications_widget.notifications[0].level == "info"
    assert notifications_widget.notifications[0].duration == 3000

    # Push another notification
    notifications_widget.push("Another notification", level="warning")

    # Check if the second notification was added
    assert len(notifications_widget.notifications) == 2
    assert notifications_widget.notifications[1].message == "Another notification"
    assert notifications_widget.notifications[1].level == "warning"
    assert notifications_widget.notifications[1].duration == 5000  # Default duration
