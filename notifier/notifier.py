from plyer import notification
import time
import threading
import heapq

class Notifier:
    """
    A class to handle desktop notifications.
    """

    def __init__(self):
        """
        Initialize the Notifier.
        """
        self.notifications = []
        self.to_remove = set()
        self.lock = threading.Lock()
        self.new_notification_event = threading.Event()

    def add_notification(self, title, message, notify_time):
        """
        Add a new notification.

        Parameters:
        title (str): The title of the notification.
        message (str): The message of the notification.
        notify_time (float): The time at which to show the notification (in seconds since epoch).
        """
        with self.lock:
            heapq.heappush(self.notifications, (notify_time, title, message))
            self.new_notification_event.set()

    def remove_notification(self, title, message):
        """
        Mark a notification for removal.

        Parameters:
        title (str): The title of the notification.
        message (str): The message of the notification.
        """
        with self.lock:
            self.to_remove.add((title, message))
            self.new_notification_event.set()

    def start(self):
        """
        Start the notification loop in a background thread.
        """
        notification_thread = threading.Thread(target=self._notification_loop)
        notification_thread.daemon = True
        notification_thread.start()

    def _notification_loop(self):
        """
        The loop that checks for notifications and shows them at the appropriate time.
        """
        while True:
            with self.lock:
                if not self.notifications:
                    next_notify_time = None
                else:
                    next_notify_time, title, message = self.notifications[0]

            if next_notify_time is None:
                # No notifications, wait indefinitely until a new one is added
                self.new_notification_event.wait()
                self.new_notification_event.clear()
            else:
                current_time = time.time()
                if current_time >= next_notify_time:
                    with self.lock:
                        heapq.heappop(self.notifications)
                        if (title, message) in self.to_remove:
                            self.to_remove.remove((title, message))
                        else:
                            notification.notify(
                                title=title,
                                message=message,
                                timeout=10
                            )
                else:
                    # Wait until the next notification time or until a new notification is added
                    wait_time = next_notify_time - current_time
                    self.new_notification_event.wait(timeout=wait_time)
                    self.new_notification_event.clear()

if __name__ == "__main__":
    # 示例用法
    notifier = Notifier()
    notifier.add_notification("Test Title", "Test Message", time.time() + 5)  # 5秒后显示通知
    notifier.start()

    # 添加更多通知
    notifier.add_notification("Another Title", "Another Message", time.time() + 10)  # 10秒后显示通知

    # 删除一个通知
    time.sleep(3)
    notifier.remove_notification("Test Title", "Test Message")

    # 保持主线程运行，以便后台线程可以继续工作
    while True:
        time.sleep(1)