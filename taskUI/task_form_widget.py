from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QDateTimeEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from taskdb import Priority

class TaskFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

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
        self.add_button.clicked.connect(self.parent.add_task)
        form_layout.addWidget(self.add_button)

        self.update_button = QPushButton('Update Task')
        self.update_button.clicked.connect(self.parent.update_task)
        form_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton('Delete Task')
        self.delete_button.clicked.connect(self.parent.delete_task)
        form_layout.addWidget(self.delete_button)

        self.setLayout(form_layout)

        # Initially hide update and delete buttons
        self.update_button.hide()
        self.delete_button.hide()

    def add_task(self):
        name = self.name_input.text()
        priority_str = self.priority_input.text()
        due_date = self.due_date_input.dateTime().toString('yyyy-MM-dd HH:mm')

        try:
            priority = Priority.from_string(priority_str)
            task_id = self.parent.task_manager.add_task(name, priority, due_date)
            self.parent.load_tasks()
            # Clear input fields after adding task
            self.clear_inputs()
            # Show add button and hide update and delete buttons
            self.show_add_button()
            self.parent.is_add_mode = True
            self.parent.current_task_id = None
        except ValueError as e:
            print(e)  # Handle invalid priority

    def update_task(self):
        if not self.parent.current_task_id:
            return

        name = self.name_input.text()
        priority_str = self.priority_input.text()
        due_date = self.due_date_input.dateTime().toString('yyyy-MM-dd HH:mm')

        try:
            priority = Priority.from_string(priority_str)
            self.parent.task_manager.update_task(self.parent.current_task_id, name, priority, due_date)
            self.parent.load_tasks()
            # Clear input fields after updating task
            self.clear_inputs()
            # Show add button and hide update and delete buttons
            self.show_add_button()
            self.parent.is_add_mode = True
            self.parent.current_task_id = None
        except ValueError as e:
            print(e)  # Handle invalid priority

    def delete_task(self):
        if not self.parent.current_task_id:
            return

        self.parent.task_manager.delete_task(self.parent.current_task_id)
        self.parent.load_tasks()
        # Clear input fields after deleting task
        self.clear_inputs()
        # Show add button and hide update and delete buttons
        self.show_add_button()
        self.parent.is_add_mode = True
        self.parent.current_task_id = None

    def on_task_clicked(self):
        selected_item = self.parent.task_list_widget.currentItem()
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
            self.show_update_delete_buttons()
            
            # Store the current task ID
            self.parent.current_task_id = task_id

    def on_task_double_clicked(self):
        selected_item = self.parent.task_list_widget.currentItem()
        if selected_item:
            task_id = selected_item.data(Qt.UserRole)  # Retrieve task_id from item data
            if task_id:
                # Open the description file for the selected task
                try:
                    self.parent.task_manager.open_description_file(task_id)
                except Exception as e:
                    print(e)  # Handle any errors that occur while opening the file

    def clear_inputs(self):
        """
        Clear the input fields.
        """
        self.name_input.clear()
        self.priority_input.clear()
        self.due_date_input.setDateTime(QDateTime.currentDateTime())

    def show_add_button(self):
        """
        Show the add button and hide the update and delete buttons.
        """
        self.add_button.show()
        self.update_button.hide()
        self.delete_button.hide()

    def show_update_delete_buttons(self):
        """
        Show the update and delete buttons and hide the add button.
        """
        self.add_button.hide()
        self.update_button.show()
        self.delete_button.show()