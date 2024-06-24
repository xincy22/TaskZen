import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListView,
    QLineEdit,
    QPushButton
)
from PyQt5.QtCore import (
    QStringListModel,
    QModelIndex,
    Qt,
    QPoint
)
from taskdb import TaskManager
from chat import TaskGenerator


class TaskListModel(QStringListModel):
    def __init__(self, parent=None):
        super(TaskListModel, self).__init__(parent)
        self.task_data = [{}]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.task_data[index.row()]['display']
        return super(TaskListModel, self).data(index, role)

    def set_tasks(self, tasks):
        self.task_data = [{
            'id': task[0],
            'display': f"{task[1]} - {task[3]} - {task[2]}"
        } for task in tasks]
        self.setStringList([task['display'] for task in self.task_data])

    def get_task_id(self, index):
        return self.task_data[index.row()]['id']


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 初始化任务管理器
        self.task_manager = TaskManager()
        # 初始化LLM
        self.chat_model = TaskGenerator()

        # 主窗口相关
        self.setWindowTitle("My App")
        self.resize(900, 600)
        self.setMinimumSize(200, 400)

        # 窗口中心组件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局
        # 垂直布局用来排列任务
        self.vertical_layout = QVBoxLayout(self.central_widget)

        # 创建任务列表视图
        self.list_view = QListView(self.central_widget)
        self.vertical_layout.addWidget(self.list_view)

        # 创建水平布局
        # 水平布局用来排布输入框和按钮
        self.horizontal_layout = QHBoxLayout()
        # 文本输入框
        self.line_edit = QLineEdit(self.central_widget)
        self.horizontal_layout.addWidget(self.line_edit)
        # 按钮
        self.push_button = QPushButton("新建任务", self.central_widget)
        self.horizontal_layout.addWidget(self.push_button)

        # 水平布局添加到垂直布局之中
        self.vertical_layout.addLayout(self.horizontal_layout)

        # 初始化任务列表视图
        self.task_model = TaskListModel()
        self.list_view.setModel(self.task_model)

        # 连接信号和槽
        self.push_button.clicked.connect(self.add_task)
        self.list_view.clicked.connect(self.on_task_clicked)
        self.list_view.doubleClicked.connect(self.on_task_double_clicked)

        self.current_task_id = None
        self.load_tasks()

    def load_tasks(self):
        tasks = self.task_manager.get_tasks()
        # 展示任务的名称、due time和priority
        self.task_model.setStringList([f"{task[1]} - {task[3]} - {task[2]}" for task in tasks])

    def add_task(self):
        user_input = self.line_edit.text()
        if user_input:
            name, priority, due_date = self.chat_model.generate(user_input)
            self.current_task_id = self.task_manager.add_task(name, priority, due_date)
            self.load_tasks()
            self.line_edit.clear()

    def update_task(self):
        user_input = self.line_edit.text()
        if user_input:
            fname, fpriority, fdue_date = self.task_manager.get_task_by_id(self.current_task_id)
            name, priority, due_date = self.chat_model.generate(f"""
            原任务为{fname}，优先级为{fpriority}，截止日期为{fdue_date}，现在用户需要对它进行如下修改：\n{user_input}
            """)
            self.task_manager.update_task(self.current_task_id, name, priority, due_date)
            self.load_tasks()
            self.line_edit.clear()

    def delete_task(self):
        if self.current_task_id:
            self.task_manager.delete_task(self.current_task_id)
            self.load_tasks()
            self.current_task_id = None

    def on_task_clicked(self, index: QModelIndex):
        task_id = self.task_model.get_task_id(index)

        if task_id:
            self.current_task_id = task_id

            self.push_button.hide()

            if not hasattr(self, 'update_button'):
                self.update_button = QPushButton("修改任务", self.central_widget)
                self.horizontal_layout.addWidget(self.update_button)
                self.update_button.clicked.connect(self.update_task)
            else:
                self.update_button.show()

            if not hasattr(self, 'delete_button'):
                self.delete_button = QPushButton("删除任务", self.central_widget)
                self.horizontal_layout.addWidget(self.delete_button)
                self.delete_button.clicked.connect(self.delete_task)
            else:
                self.delete_button.show()

    def on_task_double_clicked(self):
        pass

    def save_task_changes(self):
        pass

    def discard_task_changes(self):
        pass

    def open_context_menu(self, position: QPoint):
        pass
