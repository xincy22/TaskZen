import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QDesktopWidget
)
from PyQt5.QtCore import (
    Qt, QEvent, QFile
)
from .config import INPUT_WINDOW_STYLE_PATH
from chat import task_generator
from taskdb import task_manager


class InputWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.task_id = None

        self.parent = parent

        self.setWindowTitle('用户输入')

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.SplashScreen)
        self.setGeometry(0, 0, 700, 65)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.load_stylesheet()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('开始输入...')
        self.input_box.setFixedHeight(65)
        main_layout.addWidget(self.input_box)

        self.setLayout(main_layout)
        self.center()

        self.installEventFilter(self)


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - 700) // 2, (screen.height() - 65) // 3)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.hide()
        return super().eventFilter(obj, event)

    def load_stylesheet(self):
        style_file = QFile(INPUT_WINDOW_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.setStyleSheet(style_file.readAll().data().decode())

    def insert_task(self):
        user_prompt = self.input_box.text()
        if user_prompt:
            task_name, priority, due_date = task_generator.chat(user_prompt)
            print(task_name, priority, due_date)
            task_manager.insert_task(task_name, priority, due_date)
        self.parent.load_tasks()
        self.input_box.clear()
        self.hide()
        self.parent.list_widget.clearSelection()

    def edit_task(self):
        user_prompt = self.input_box.text()
        if user_prompt:
            ptask = task_manager.get_task_by_id(self.task_id)
            task_name, priority, due_date = task_generator.chat(f"""
            我需要你依据{user_prompt}调整现有的{ptask}任务
            """)
            print(task_name, priority, due_date)
            task_manager.update_task(self.task_id, task_name, priority, due_date)
        self.parent.load_tasks()
        self.input_box.clear()
        self.hide()


