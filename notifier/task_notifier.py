from datetime import datetime, timedelta
from .notifier import Notifier

class TaskNotifier:
    """
    A class to handle task notifications.
    """

    def __init__(self):
        """
        Initialize the TaskNotifier.
        """
        self.notifier = Notifier()
        self.notifier.start()

    def set_task_notifications(self, task_id, name, due_date):
        """
        Set notifications for a task.

        Parameters:
        task_id (int): The ID of the task.
        name (str): The name of the task.
        due_date (str): The due date of the task in the format 'YYYY-MM-DD HH:MM'.
        """
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        reminder_times = self._calculate_reminder_times(due_date_obj)
        
        for reminder_time in reminder_times:
            if reminder_time > datetime.now():
                title = f"Reminder: {name} (Task ID: {task_id})"
                message = f"Task '{name}' is due on {due_date}"
                self.notifier.add_notification(
                    title=title,
                    message=message,
                    notify_time=reminder_time.timestamp()
                )

    def update_task_notifications(self, task_id, current_name, current_due_date, name, due_date):
        """
        Update notifications for a task.

        Parameters:
        task_id (int): The ID of the task.
        current_name (str): The current name of the task.
        current_due_date (str): The current due date of the task in the format 'YYYY-MM-DD HH:MM'.
        name (str): The new name of the task.
        due_date (str): The new due date of the task in the format 'YYYY-MM-DD HH:MM'.
        """
        self.delete_task_notifications(task_id, current_name, current_due_date)
        self.set_task_notifications(task_id, name, due_date)

    def delete_task_notifications(self, task_id, name, due_date):
        """
        Delete notifications for a task.

        Parameters:
        task_id (int): The ID of the task.
        name (str): The name of the task.
        due_date (str): The due date of the task in the format 'YYYY-MM-DD HH:MM'.
        """
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        reminder_times = self._calculate_reminder_times(due_date_obj)
        
        for reminder_time in reminder_times:
            if reminder_time > datetime.now():
                title = f"Reminder: {name} (Task ID: {task_id})"
                message = f"Task '{name}' is due on {due_date}"
                self.notifier.remove_notification(title, message)

    def _calculate_reminder_times(self, due_date_obj):
        """
        Calculate all possible reminder times based on the due date.

        Parameters:
        due_date_obj (datetime): The due date as a datetime object.

        Returns:
        list: A list of datetime objects representing the reminder times.
        """
        return [
            due_date_obj - timedelta(minutes=10),
            due_date_obj - timedelta(minutes=30),
            due_date_obj - timedelta(hours=1),
            due_date_obj - timedelta(hours=2),
            due_date_obj - timedelta(hours=5),
            due_date_obj.replace(hour=8, minute=0) if due_date_obj.hour >= 8 else due_date_obj - timedelta(days=1),
            due_date_obj - timedelta(days=1),
            due_date_obj - timedelta(days=2),
            due_date_obj - timedelta(days=5),
            due_date_obj - timedelta(weeks=1),
            due_date_obj - timedelta(weeks=2),
            due_date_obj - timedelta(days=30)
        ]

if __name__ == "__main__":
    # 示例用法
    task_notifier = TaskNotifier()
    task_notifier.set_task_notifications(1, "Test Task", "2024-06-12 14:00")  # 设置任务通知

    # 更新任务通知
    task_notifier.update_task_notifications(1, "Test Task", "2024-06-12 14:00", "Updated Task", "2024-06-13 14:00")

    # 删除任务通知
    task_notifier.delete_task_notifications(1, "Updated Task", "2024-06-13 14:00")