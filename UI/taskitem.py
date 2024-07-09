from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QMenu, QAction
)
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QFont
from taskdb import task_manager
from .config import TASKITEM_STYLE_PATH, MENU_STYLE_PATH


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

        self.menu = QMenu(self)
        self.info_action = QAction("taskZen 2.0", parent)
        self.info_action.setEnabled(False)
        self.menu.addAction(self.info_action)
        self.menu.addAction("删除", lambda: self.delete())
        self.menu.addAction("修改", lambda: self.parent.edit(self.task_id))

        self.load_stylesheet()

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def set_label_text(self, task_name=None, priority=None, due_date=None):
        if task_name is not None:
            self.task_name_label.setText(task_name)
        if priority is not None:
            self.priority_label.setText(priority)
        if due_date is not None:
            self.due_date_label.setText(due_date)

    def delete(self):
        task_id = self.task_id
        task_manager.delete_task(task_id)
        self.parent.load_tasks()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.delete()

    def load_stylesheet(self):

        style_file = QFile(TASKITEM_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.setStyleSheet(style_file.readAll().data().decode())

        menu_style_file = QFile(MENU_STYLE_PATH)
        menu_style_file.open(QFile.ReadOnly)
        self.menu.setStyleSheet(menu_style_file.readAll().data().decode())
        self.menu.setWindowFlag(Qt.FramelessWindowHint)
        self.menu.setWindowFlag(Qt.NoDropShadowWindowHint)
        self.menu.setAttribute(Qt.WA_TranslucentBackground)

