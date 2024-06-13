import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from taskdb import TaskManager
from .tray_icon import TrayIcon
from .task_list_widget import TaskListWidget
from .task_form_widget import TaskFormWidget
from config import ICON_PATH

class TaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.initUI()
        self.tray_icon = TrayIcon(self)
        self.old_pos = None  # 用于存储鼠标按下时的位置
        self.is_add_mode = True  # 用于跟踪当前是否处于添加任务模式
        self.current_task_id = None  # 用于存储当前选中的任务ID

    def initUI(self):
        self.setWindowTitle('TaskZen')
        self.setGeometry(100, 100, 800, 600)
        
        # Set window to be frameless and translucent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set window icon
        self.setWindowIcon(QIcon(ICON_PATH))

        # Main layout
        main_layout = QVBoxLayout()

        # Task list widget
        self.task_list_widget = TaskListWidget(self)
        main_layout.addWidget(self.task_list_widget)

        # Task form widget
        self.task_form_widget = TaskFormWidget(self)
        main_layout.addWidget(self.task_form_widget)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background: rgba(255, 255, 255, 0.8); border-radius: 10px;")
        
        # Set central widget
        self.setCentralWidget(container)

        # Load tasks
        self.load_tasks()

    def load_tasks(self):
        self.task_list_widget.load_tasks()

    def add_task(self):
        self.task_form_widget.add_task()

    def update_task(self):
        self.task_form_widget.update_task()

    def delete_task(self):
        self.task_form_widget.delete_task()

    def on_task_clicked(self):
        self.task_form_widget.on_task_clicked()

    def on_task_double_clicked(self):
        self.task_form_widget.on_task_double_clicked()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_item = QApplication.widgetAt(event.globalPos())
            if not isinstance(clicked_item, QListWidget) and not isinstance(clicked_item.parent(), QListWidget):
                # Clicked outside the task list or on an empty area of the list
                if not self.is_add_mode:
                    self.reset_to_add_mode()

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress and source is self.task_list_widget.viewport():
            item = self.task_list_widget.itemAt(event.pos())
            if item is None:
                # Clicked on empty area of the task list
                if not self.is_add_mode:
                    self.reset_to_add_mode()
        return super().eventFilter(source, event)

    def reset_to_add_mode(self):
        # Clear input fields and reset to add mode
        if not self.is_add_mode:
            # Clear input fields
            self.task_form_widget.clear_inputs()
            
            # Show add button and hide update and delete buttons
            self.task_form_widget.show_add_button()
            
            # Set mode to add
            self.is_add_mode = True
            
            # Clear the current task ID
            self.current_task_id = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManagerUI()
    ex.show()
    sys.exit(app.exec_())