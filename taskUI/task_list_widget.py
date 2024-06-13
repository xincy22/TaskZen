from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class TaskListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.itemClicked.connect(self.parent.on_task_clicked)
        self.itemDoubleClicked.connect(self.parent.on_task_double_clicked)
        print(f"TaskListWidget initialized with parent: {self.parent}")

    def load_tasks(self):
        self.clear()
        tasks = self.parent.task_manager.get_tasks()
        for task in tasks:
            task_id, name, priority, due_date, description_file = task
            item = QListWidgetItem(f'{name} - {priority} - {due_date}')
            item.setData(Qt.UserRole, task_id)  # Store task_id in item data
            self.addItem(item)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        item = self.itemAt(event.pos())
        if item is None:
            # Clicked on empty area of the task list
            self.parent.reset_to_add_mode()