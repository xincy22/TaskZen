import sqlite3
import os
import subprocess
from datetime import datetime
from .priority import Priority
from config import DATABASE_PATH, DESCRIPTION_DIR
from notifier import TaskNotifier


class TaskManager:
    def __init__(self):
        self.db_name = DATABASE_PATH
        self.description_dir = DESCRIPTION_DIR
        self.task_notifier = TaskNotifier()
        self._create_table()

    def _create_table(self):
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
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS tasks')
        conn.commit()
        self._create_table()
        conn.close()

    def _create_description_file(self, task_id, name, due_date):
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            month = due_date_obj.strftime("%B")
            sanitized_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(' ', '_')
            filename = f"{task_id}_{sanitized_name}_{month}.md"
            filepath = os.path.join(self.description_dir, filename)

            with open(filepath, 'w') as f:
                f.write(f"# {name}\n\n")
                f.write("## Description\n\n")
                f.write("Describe the task here.\n")

            return filepath

        except Exception as e:
            print(f"Error creating description file: {e}")
            return None

    def add_task(self, name, priority, due_date):
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

        self.task_notifier.set_task_notifications(task_id, name, due_date)

        return task_id

    def get_tasks(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        conn.close()
        return tasks

    def update_task(self, task_id, name, priority, due_date):
        if not isinstance(priority, Priority):
            raise ValueError("priority must be an instance of Priority enum")

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT name, due_date FROM tasks WHERE id=?", (task_id,))
        current_name, current_due_date = c.fetchone()

        c.execute("UPDATE tasks SET name=?, priority=?, due_date=? WHERE id=?",
                  (name, str(priority), due_date, task_id))

        conn.commit()
        conn.close()

        self.task_notifier.update_task_notifications(task_id, current_name, current_due_date, name, due_date)

    def delete_task(self, task_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT name, due_date, description_file FROM tasks WHERE id=?", (task_id,))
        result = c.fetchone()
        if result is None:
            conn.close()
            return

        current_name, current_due_date, description_file = result

        if description_file and os.path.exists(description_file):
            os.remove(description_file)

        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

        self.task_notifier.delete_task_notifications(task_id, current_name, current_due_date)

    def open_description_file(self, task_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT description_file FROM tasks WHERE id=?", (task_id,))
        description_file = c.fetchone()[0]

        if description_file and os.path.exists(description_file):
            if os.name == 'nt':
                os.startfile(description_file)
            elif os.name == 'posix':
                subprocess.call(
                    ('open', description_file) if sys.platform == 'darwin' else ('xdg-open', description_file))

    def get_task_by_id(self, task_id):
        """
        Retrieve a task by its ID.

        Parameters:
        task_id (int): The ID of the task to retrieve.

        Returns:
        tuple: A tuple representing the task (id, name, priority, due_date).
               Returns None if the task is not found.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, name, priority, due_date FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
        conn.close()

        return task
