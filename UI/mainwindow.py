from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QLabel,
    QListWidgetItem,
)
from PyQt5.QtCore import (
    QStringListModel,
    QModelIndex,
    Qt,
    QPoint,
    QFile,
)
from PyQt5.QtGui import QFont
from .config import (
    MAIN_WINDOW_STYLE_PATH, TASKITEM_STYLE_PATH, FONT_PATH
)
from .resizable_frame import ResizableFrame
from .inputwindow import InputWindow
from taskdb import task_manager


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clearSelection()
        self.parent().mousePressEvent(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.parent().mouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.parent().mouseReleaseEvent(event)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.parent().mouseDoubleClickEvent(event)
        super().mouseDoubleClickEvent(event)


class TaskItemWidget(QWidget):
    def __init__(self, task_id, task_name, priority, due_date, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.parent = parent
        self.task_name_label = QLabel(task_name, objectName="task_name_label")
        self.priority_label = QLabel(priority, objectName="priority_label")
        self.due_date_label = QLabel(due_date, objectName="due_date_label")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.task_name_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.priority_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.due_date_label, alignment=Qt.AlignCenter)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.layout)

        self.setup_UI()

    def set_label_text(self, task_name=None, priority=None, due_date=None):
        if task_name is not None:
            self.task_name_label.setText(task_name)
        if priority is not None:
            self.priority_label.setText(priority)
        if due_date is not None:
            self.due_date_label.setText(due_date)

    def mouseDoubleClickEvent(self, event):
        task_id = self.task_id
        task_manager.delete_task(task_id)
        self.parent.load_tasks()
        print("reached double clicked event")

    def setup_UI(self):
        font = QFont(FONT_PATH, 18)

        style_file = QFile(TASKITEM_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.setStyleSheet(style_file.readAll().data().decode())

        self.task_name_label.setFont(font)
        self.priority_label.setFont(font)
        self.due_date_label.setFont(font)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resizable_frame = ResizableFrame(self)

        self.setWindowTitle('taskZen - 让任务管理成为一种习惯')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setWindowOpacity(1)
        self.resize(800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMouseTracking(True)
        self.setMouseTracking(True)

        self.list_widget = CustomListWidget(self.central_widget)
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.addWidget(self.list_widget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_UI()

        self.input_window = InputWindow(self)
        self.input_window.hide()

        self.load_tasks()

    def setup_UI(self):
        style_file = QFile(MAIN_WINDOW_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.setStyleSheet(style_file.readAll().data().decode())

    def mousePressEvent(self, event):
        self.resizable_frame.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.resizable_frame.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizable_frame.mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        print("reached input window show")
        self.input_window.show()

    def load_tasks(self):
        self.list_widget.clear()
        tasks = task_manager.list_tasks()
        for task in tasks:
            task_widget = TaskItemWidget(*task, parent=self)
            task_item = QListWidgetItem(self.list_widget)
            task_item.setSizeHint(task_widget.sizeHint())
            self.list_widget.addItem(task_item)
            self.list_widget.setItemWidget(task_item, task_widget)