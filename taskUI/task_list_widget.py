from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class TaskListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.itemClicked.connect(self.parent.on_task_clicked)
        self.itemDoubleClicked.connect(self.parent.on_task_double_clicked)
        self.viewport().installEventFilter(self.parent)

    def load_tasks(self):
        self.clear()
        tasks = self.parent.task_manager.get_tasks()
        for task in tasks:
            task_id, name, priority, due_date, description_file = task
            item = QListWidgetItem(f'{name} - {priority} - {due_date}')
            item.setData(Qt.UserRole, task_id)  # Store task_id in item data
            self.addItem(item)