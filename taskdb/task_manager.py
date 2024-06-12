import sqlite3
from .priority import Priority

class TaskManager:
    """
    A class to manage tasks using an SQLite database.
    """

    def __init__(self, db_name='taskdb/tasks.db'):
        """
        Initialize the TaskManager with a database name.

        Parameters:
        db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
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
            due_date TEXT NOT NULL
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

    def add_task(self, name, priority, due_date):
        """
        Add a new task to the database.

        Parameters:
        name (str): The name of the task.
        priority (Priority): The priority of the task.
        due_date (str): The due date of the task.

        Raises:
        ValueError: If priority is not an instance of Priority enum.
        """
        if not isinstance(priority, Priority):
            raise ValueError("priority must be an instance of Priority enum")
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (name, priority, due_date) VALUES (?, ?, ?)", (name, str(priority), due_date))
        conn.commit()
        conn.close()

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
        c.execute("UPDATE tasks SET name=?, priority=?, due_date=? WHERE id=?", (name, str(priority), due_date, task_id))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        """
        Delete a task from the database.

        Parameters:
        task_id (int): The ID of the task to delete.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # 创建任务管理器实例
    task_manager = TaskManager()

    # 初始化数据库
    task_manager.initialize_database()

    # 添加任务
    task_manager.add_task('Finish project', Priority.HIGH, '2024-06-30')

    # 获取并打印所有任务
    tasks = task_manager.get_tasks()
    for task in tasks:
        print(task)

    # 更新任务
    task_manager.update_task(1, 'Finish project update', Priority.MEDIUM, '2024-07-01')

    # 删除任务
    task_manager.delete_task(1)