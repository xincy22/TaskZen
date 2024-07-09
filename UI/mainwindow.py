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
    QAction,
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
    MAIN_WINDOW_STYLE_PATH, TASKITEM_STYLE_PATH, MENU_STYLE_PATH,
    LIST_WIDGET_STYLE_PATH
)
from .resizable_frame import ResizableFrame
from .inputwindow import InputWindow
from taskdb import task_manager
from .taskitem import TaskItemWidget
from .tray_icon import TrayIcon


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.menu = QMenu(self)

        self.info_action = QAction("taskZen 2.0", self)
        self.info_action.setEnabled(False)
        self.menu.addAction(self.info_action)
        self.menu.addAction("添加任务", lambda: self.parent().parent().input_window.show())
        self.menu.addAction("隐藏到托盘", lambda: self.parent().parent().hide())
        self.menu.addAction("关闭软件", lambda: self.parent().parent().quit())

        self.load_stylesheet()

    def load_stylesheet(self):

        style_file = QFile(LIST_WIDGET_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.setStyleSheet(style_file.readAll().data().decode())

        menu_style_file = QFile(MENU_STYLE_PATH)
        menu_style_file.open(QFile.ReadOnly)
        self.menu.setStyleSheet(menu_style_file.readAll().data().decode())
        self.menu.setWindowFlag(Qt.FramelessWindowHint)
        self.menu.setWindowFlag(Qt.NoDropShadowWindowHint)
        self.menu.setAttribute(Qt.WA_TranslucentBackground)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resizable_frame = ResizableFrame(self)

        self.setWindowTitle('taskZen - 让任务管理成为一种习惯')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        self.resize(800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMouseTracking(True)
        self.setMouseTracking(True)

        self.tray_icon = TrayIcon(self)

        self.list_widget = CustomListWidget(self.central_widget)
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.addWidget(self.list_widget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.load_stylesheet()

        self.input_window = InputWindow(self)
        self.input_window.input_box.returnPressed.connect(self.input_window.insert_task)
        self.input_window.hide()

        self.edit_window = InputWindow(self)
        self.edit_window.input_box.returnPressed.connect(self.edit_window.edit_task)
        self.edit_window.hide()

        self.load_tasks()

    def load_stylesheet(self):
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

    def edit(self, task_id):
        self.edit_window.task_id = task_id
        self.edit_window.show()

    def quit(self):
        self.tray_icon.hide()
        self.close()
        QApplication.quit()