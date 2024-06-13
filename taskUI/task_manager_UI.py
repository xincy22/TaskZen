import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from taskdb import TaskManager
from .tray_icon import TrayIcon
from .task_list_widget import TaskListWidget
from .task_form_widget import TaskFormWidget
from config import ICON_PATH, STYLE_PATH

class TaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.initUI()
        self.tray_icon = TrayIcon(self)
        self.old_pos = None 
        self.is_add_mode = True 
        self.current_task_id = None 

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
        main_layout.setSpacing(10)  # Set spacing between widgets
        main_layout.setContentsMargins(10, 10, 10, 10)  # Set margins around the layout

        # Task list widget
        self.task_list_widget = TaskListWidget(self)
        main_layout.addWidget(self.task_list_widget)

        # Task form widget
        self.task_form_widget = TaskFormWidget(self)
        main_layout.addWidget(self.task_form_widget)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        container.setObjectName("centralWidget")
        
        # Set central widget
        self.setCentralWidget(container)

        # Load tasks
        self.load_tasks()

        # Apply flat design styles
        self.apply_styles()

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
        # Set mode to update when a task is clicked
        self.is_add_mode = False

    def on_task_double_clicked(self):
        self.task_form_widget.on_task_double_clicked()
        # Set mode to update when a task is double-clicked
        self.is_add_mode = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            item = self.task_list_widget.itemAt(event.pos())
            if item is None:
                # Clicked on empty area of the task list
                self.reset_to_add_mode()

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

    def apply_styles(self):
        """
        Apply flat design styles to the UI components.
        """
        with open(STYLE_PATH, "r") as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManagerUI()
    ex.show()
    sys.exit(app.exec_())