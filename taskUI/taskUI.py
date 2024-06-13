import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QLabel, QHBoxLayout, QDateTimeEdit)
from PyQt5.QtCore import QDateTime, Qt, QPoint
from PyQt5.QtGui import QIcon
from taskdb import TaskManager, Priority
from .tray_icon import TrayIcon

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
        self.setWindowIcon(QIcon("taskZen.ico"))

        # Main layout
        main_layout = QVBoxLayout()

        # Task list
        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.on_task_clicked)
        self.task_list.itemDoubleClicked.connect(self.on_task_double_clicked)
        self.task_list.viewport().installEventFilter(self)
        main_layout.addWidget(self.task_list)

        # Form layout for adding/updating tasks
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Task Name')
        form_layout.addWidget(self.name_input)

        self.priority_input = QLineEdit()
        self.priority_input.setPlaceholderText('Priority (High, Medium, Low)')
        form_layout.addWidget(self.priority_input)

        self.due_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.due_date_input.setDisplayFormat('yyyy-MM-dd HH:mm')
        form_layout.addWidget(self.due_date_input)

        self.add_button = QPushButton('Add Task')
        self.add_button.clicked.connect(self.add_task)
        form_layout.addWidget(self.add_button)

        self.update_button = QPushButton('Update Task')
        self.update_button.clicked.connect(self.update_task)
        form_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton('Delete Task')
        self.delete_button.clicked.connect(self.delete_task)
        form_layout.addWidget(self.delete_button)

        main_layout.addLayout(form_layout)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background: rgba(255, 255, 255, 0.8); border-radius: 10px;")
        
        # Set central widget
        self.setCentralWidget(container)

        # Initially hide update and delete buttons
        self.update_button.hide()
        self.delete_button.hide()

        # Load tasks
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            task_id, name, priority, due_date, description_file = task
            item = QListWidgetItem(f'{name} - {priority} - {due_date}')
            item.setData(Qt.UserRole, task_id)  # Store task_id in item data
            self.task_list.addItem(item)

    def add_task(self):
        name = self.name_input.text()
        priority_str = self.priority_input.text()
        due_date = self.due_date_input.dateTime().toString('yyyy-MM-dd HH:mm')

        try:
            priority = Priority.from_string(priority_str)
            task_id = self.task_manager.add_task(name, priority, due_date)
            self.load_tasks()
            # Clear input fields after adding task
            self.name_input.clear()
            self.priority_input.clear()
            self.due_date_input.setDateTime(QDateTime.currentDateTime())
            # Show add button and hide update and delete buttons
            self.is_add_mode = True
            self.add_button.show()
            self.update_button.hide()
            self.delete_button.hide()
            self.current_task_id = None
        except ValueError as e:
            print(e)  # Handle invalid priority

    def update_task(self):
         if not self.current_task_id:
             return

         name = self.name_input.text()
         priority_str = self.priority_input.text()
         due_date = self.due_date_input.dateTime().toString('yyyy-MM-dd HH:mm')

         try:
             priority = Priority.from_string(priority_str)
             self.task_manager.update_task(self.current_task_id, name, priority, due_date)
             self.load_tasks()
             # Clear input fields after updating task
             self.name_input.clear()
             self.priority_input.clear()
             self.due_date_input.setDateTime(QDateTime.currentDateTime())
             # Show add button and hide update and delete buttons
             self.is_add_mode = True
             self.add_button.show()
             self.update_button.hide()
             self.delete_button.hide()
             self.current_task_id = None
         except ValueError as e:
             print(e)  # Handle invalid priority

    def delete_task(self):
         if not self.current_task_id:
             return

         self.task_manager.delete_task(self.current_task_id)
         self.load_tasks()
         # Clear input fields after deleting task
         self.name_input.clear()
         self.priority_input.clear()
         self.due_date_input.setDateTime(QDateTime.currentDateTime())
         # Show add button and hide update and delete buttons
         self.is_add_mode = True
         self.add_button.show()
         self.update_button.hide()
         self.delete_button.hide()
         self.current_task_id = None

    def on_task_clicked(self):
         # Show update and delete buttons and hide add button when a task is clicked
         selected_item = self.task_list.currentItem()
         if selected_item:
             task_text = selected_item.text()
             name, priority_str, due_date = task_text.split(' - ')
             task_id = selected_item.data(Qt.UserRole)  # Retrieve task_id from item data
             
             # Populate input fields with selected task details
             self.name_input.setText(name)
             self.priority_input.setText(priority_str)
             due_date_obj = QDateTime.fromString(due_date, 'yyyy-MM-dd HH:mm')
             if due_date_obj.isValid():
                 self.due_date_input.setDateTime(due_date_obj)
             
             # Show update and delete buttons and hide add button
             self.is_add_mode = False
             self.add_button.hide()
             self.update_button.show()
             self.delete_button.show()
             
             # Store the current task ID
             self.current_task_id = task_id

    def on_task_double_clicked(self):
         selected_item = self.task_list.currentItem()
         if selected_item:
             task_id = selected_item.data(Qt.UserRole)  # Retrieve task_id from item data
             if task_id:
                 # Open the description file for the selected task
                 try:
                     self.task_manager.open_description_file(task_id)
                 except Exception as e:
                     print(e)  # Handle any errors that occur while opening the file

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
         if event.type() == event.MouseButtonPress and source is self.task_list.viewport():
             item = self.task_list.itemAt(event.pos())
             if item is None:
                 # Clicked on empty area of the task list
                 if not self.is_add_mode:
                     self.reset_to_add_mode()
         return super().eventFilter(source, event)

    def reset_to_add_mode(self):
        # Clear input fields and reset to add mode
        if not self.is_add_mode:
            # Clear input fields
            self.name_input.clear()
            self.priority_input.clear()
            self.due_date_input.setDateTime(QDateTime.currentDateTime())
            
            # Show add button and hide update and delete buttons
            self.add_button.show()
            self.update_button.hide()
            self.delete_button.hide()
            
            # Set mode to add
            self.is_add_mode = True
            
            # Clear the current task ID
            self.current_task_id = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManagerUI()
    ex.show()
    sys.exit(app.exec_())