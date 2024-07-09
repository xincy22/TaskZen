import sqlite3
from .config import TaskDB_PATH


class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect(TaskDB_PATH)
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL
                )
            """)


    def insert_task(self, task_name, priority, due_date):
        try:
            with self.conn:
                cursor = self.conn.execute("""
                    INSERT INTO tasks (task_name, priority, due_date)
                    VALUES (?, ?, ?)
                """, (task_name, priority, due_date))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def delete_task(self, task_id):
        with self.conn:
            self.conn.execute("""
                DELETE FROM tasks WHERE task_id = ?
            """, (task_id,))
            return task_id

    def update_task(self, task_id, task_name=None, priority=None, due_date=None):
        updates = []
        params = []
        if task_name is not None:
            updates.append("task_name = ?")
            params.append(task_name)
        if priority is not None:
            updates.append("priority = ?")
            params.append(priority)
        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date)
        params.append(task_id)

        with self.conn:
            self.conn.execute(f"""
                UPDATE tasks
                SET {", ".join(updates)}
                WHERE task_id = ?
            """, params)
            return task_id

    def list_tasks(self):
        with self.conn:
            cursor = self.conn.execute("""
                SELECT * FROM tasks
            """)
            tasks = cursor.fetchall()
            return tasks

    def get_task_by_id(self, task_id):
        with self.conn:
            cursor = self.conn.execute("""
                SELECT * FROM tasks
                WHERE task_id = ?
            """, (task_id,))
            task = cursor.fetchone()
            return task

    def __del__(self):
        self.conn.close()


task_manager = TaskManager()
