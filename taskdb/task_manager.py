import sqlite3
import os
import subprocess
from datetime import datetime
from .priority import Priority
from config import DATABASE_PATH, DESCRIPTION_DIR

class TaskManager:
    """
    A class to manage tasks using an SQLite database.
    """

    def __init__(self):
        """
        Initialize the TaskManager with a database name and description directory.
        """
        self.db_name = DATABASE_PATH
        self.description_dir = DESCRIPTION_DIR
        self._create_table()

    def _create_table(self):
        """
        Create the tasks table in the SQLite database if it doesn't exist.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            description_file TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def initialize_database(self):
        """
        Initialize the database by dropping the existing tasks table and creating a new one.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS tasks')
        conn.commit()
        self._create_table()
        conn.close()

    def _create_description_file(self, task_id, name, due_date):
        """
        Create a markdown file for the task description.

        Parameters:
        task_id (int): The ID of the task.
        name (str): The name of the task.
        due_date (str): The due date of the task.

        Returns:
        str: The path to the markdown file.
        """
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            month = due_date_obj.strftime("%B")
            filename = f"{task_id}_{month}.md"
            filepath = os.path.join(self.description_dir, filename)
            
            print(f"Creating description file at: {filepath}")  # Debug information
            
            with open(filepath, 'w') as f:
                f.write(f"# {name}\n\n")
                f.write("## Description\n\n")
                f.write("Describe the task here.\n")
            
            print(f"Successfully wrote to file: {filepath}")  # Debug information
            
            return filepath
        
        except Exception as e:
            print(f"Error creating description file: {e}")  # Debug information
            return None

    def add_task(self, name, priority, due_date):
        """
        Add a new task to the database.

        Parameters:
        name (str): The name of the task.
        priority (Priority): The priority of the task.
        due_date (str): The due date of the task.

        Returns:
        int: The ID of the newly added task.

        Raises:
        ValueError: If priority is not an instance of Priority enum.
        """
        if not isinstance(priority, Priority):
            raise ValueError("priority must be an instance of Priority enum")
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (name, priority, due_date) VALUES (?, ?, ?)", (name, str(priority), due_date))
        task_id = c.lastrowid
        description_file = self._create_description_file(task_id, name, due_date)
        
        if description_file:
            c.execute("UPDATE tasks SET description_file=? WHERE id=?", (description_file, task_id))
        
        conn.commit()
        conn.close()
        
        return task_id

    def get_tasks(self):
        """
        Retrieve all tasks from the database.

        Returns:
        list: A list of tuples representing the tasks.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        conn.close()
        return tasks

    def update_task(self, task_id, name, priority, due_date):
        """
        Update an existing task in the database.

        Parameters:
        task_id (int): The ID of the task to update.
        name (str): The new name of the task.
        priority (Priority): The new priority of the task.
        due_date (str): The new due date of the task.

        Raises:
        ValueError: If priority is not an instance of Priority enum.
        """
        if not isinstance(priority, Priority):
            raise ValueError("priority must be an instance of Priority enum")
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Update the task without changing the description file
        c.execute("UPDATE tasks SET name=?, priority=?, due_date=? WHERE id=?", 
                  (name, str(priority), due_date, task_id))
        
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        """
        Delete a task from the database.

        Parameters:
        task_id (int): The ID of the task to delete.
        """
        
        # Delete the associated description file
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT description_file FROM tasks WHERE id=?", (task_id,))
        description_file = c.fetchone()[0]
        
        if description_file and os.path.exists(description_file):
            os.remove(description_file)

        # Delete the task from the database
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

    def open_description_file(self, task_id):
        """
        Open the description file for a given task using the system's default application.

        Parameters:
        task_id (int): The ID of the task whose description file should be opened.
        """
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT description_file FROM tasks WHERE id=?", (task_id,))
        description_file = c.fetchone()[0]
        
        if description_file and os.path.exists(description_file):
            if os.name == 'nt':  # Windows
                os.startfile(description_file)
            elif os.name == 'posix':  # macOS or Linux
                subprocess.call(('open', description_file) if sys.platform == 'darwin' else ('xdg-open', description_file))