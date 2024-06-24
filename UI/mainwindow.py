import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListView,
    QLineEdit,
    QPushButton,
    QStyledItemDelegate,
    QAbstractItemDelegate,
)
from PyQt5.QtCore import (
    QStringListModel,
    QModelIndex,
    Qt,
    QPoint,
)
from taskdb import TaskManager
from chat import TaskGenerator


class TaskListModel(QStringListModel):
    def __init__(self, parent=None):
        super(TaskListModel, self).__init__(parent)
        self.task_data = []

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


class TaskDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.editing_index = None

    def paint(self, painter, option, index):
        if index.row() == self.editing_index:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            name_edit = QLineEdit(widget)
            priority_edit = QLineEdit(widget)
            due_time_edit = QLineEdit(widget)
            save_button = QPushButton("√", widget)
            discard_button = QPushButton("×", widget)

            layout.addWidget(name_edit)
            layout.addWidget(priority_edit)
            layout.addWidget(due_time_edit)
            layout.addWidget(save_button)
            layout.addWidget(discard_button)

            widget.setGeometry(option.rect)
            widget.render(painter, option.rect.topLeft())
        else:
            super(TaskDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.row() == self.editing_index:
            editor = QWidget(parent)
            layout = QHBoxLayout(editor)
            self.name_edit = QLineEdit(editor)
            self.priority_edit = QLineEdit(editor)
            self.due_time_edit = QLineEdit(editor)
            self.save_button = QPushButton("√", editor)
            self.discard_button = QPushButton("×", editor)

            layout.addWidget(self.name_edit)
            layout.addWidget(self.priority_edit)
            layout.addWidget(self.due_time_edit)
            layout.addWidget(self.save_button)
            layout.addWidget(self.discard_button)

            self.save_button.clicked.connect(self.commitAndCloseEditor)
            self.discard_button.clicked.connect(self.discardAndCloseEditor)

    def setEditorData(self, editor, index):
        if index == self.editing_index:
            task_data = index.data(Qt.DisplayRole).split(' - ')
            self.name_edit.setText(task_data[0])
            self.priority_edit.setText(task_data[1])
            self.due_time_edit.setText(task_data[2])
        else:
            super(TaskDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index == self.editing_index:
            name = self.name_edit.text()
            priority = self.priority_edit.text()
            due_time = self.due_time_edit.text()
            model.setData(index, f"{name} - {priority} - {due_time}")
        else:
            super(TaskDelegate, self).setModelData(editor, model, index)

    def commitAndCloseEditor(self):
        editor = self.sender().parent()
        main_window = editor.parent().parent().parent().parent()
        main_window.task_manager.update_task(
            main_window.current_task_id,
            self.name_edit.text(),
            self.priority_edit.text(),
            self.due_time_edit.text()
        )
        main_window.load_tasks()
        main_window.setup_UI('selected')
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QAbstractItemDelegate.NoHint)
        self.editing_index = None

    def discardAndCloseEditor(self):
        editor = self.sender().parent()
        self.closeEditor.emit(editor, QStyledItemDelegate.NoHint)
        self.editing_index = None


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 任务管理模块
        self.task_manager = TaskManager()
        self.chat_model = TaskGenerator()

        # 初始化UI
        self.setup_UI('init')

        # 窗口中心组件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 任务列表视图
        self.list_view = QListView(self.central_widget)
        self.task_model = TaskListModel()
        self.list_view.setModel(self.task_model)
        # 自定义委托
        self.task_delegate = TaskDelegate(self.list_view)
        self.list_view.setItemDelegate(self.task_delegate)

        # 任务输入部分
        self.line_edit = QLineEdit(self.central_widget)
        self.push_button = QPushButton("添加任务", self.central_widget)
        self.update_button = QPushButton("修改任务", self.central_widget)
        self.delete_button = QPushButton("删除任务", self.central_widget)

        # UI布局
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.line_edit)
        self.horizontal_layout.addWidget(self.push_button)
        self.horizontal_layout.addWidget(self.update_button)
        self.horizontal_layout.addWidget(self.delete_button)
        horizontal_container = QWidget()
        horizontal_container.setLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.list_view)
        self.vertical_layout.addWidget(horizontal_container)

        # 连接信号和槽
        self.push_button.clicked.connect(self.add_task)
        self.list_view.clicked.connect(self.on_task_clicked)
        self.list_view.doubleClicked.connect(self.on_task_double_clicked)
        self.update_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)

        # 运行初始状态设置
        self.current_task_id = None
        self.setup_UI('add')
        self.load_tasks()

    def setup_UI(self, mode='init'):
        match mode:
            case 'init':
                self.setWindowTitle("TaskZen - 让任务管理成为一种生活习惯")
                self.resize(900, 600)
                self.setMinimumSize(200, 400)
            case 'add':
                self.push_button.show()
                self.update_button.hide()
                self.delete_button.hide()
            case 'selected':
                self.push_button.hide()
                self.update_button.show()
                self.delete_button.show()

    def load_tasks(self):
        tasks = self.task_manager.get_tasks()
        self.task_model.set_tasks(tasks)

    def add_task(self):
        print("reached.")
        user_input = self.line_edit.text()
        if user_input:
            name, priority, due_date = self.chat_model.generate(user_input)
            print(f"name:{name}, priority:{priority}, due_date:{due_date}")
            self.current_task_id = self.task_manager.add_task(name, priority, due_date)
            print("任务ID", self.current_task_id)
            self.load_tasks()
            self.line_edit.clear()
            self.setup_UI('selected')

    def update_task(self):
        if self.current_task_id:
            user_input = self.line_edit.text()
            if user_input:
                fname, fpriority, fdue_date = self.task_manager.get_task_by_id(self.current_task_id)
                name, priority, due_date = self.chat_model.generate(f"""
                            原任务为{fname}，优先级为{fpriority}，截止日期为{fdue_date}，现在用户需要对它进行如下修改：\n{user_input}
                            """)
                self.task_manager.update_task(self.current_task_id, name, priority, due_date)
                self.load_tasks()
                self.line_edit.clear()
                self.setup_UI('selected')

    def delete_task(self):
        if self.current_task_id:
            self.task_manager.delete_task(self.current_task_id)
            self.load_tasks()
            self.current_task_id = None
            self.setup_UI('add')

    def on_task_clicked(self, index: QModelIndex):
        task_id = self.task_model.get_task_id(index)

        if task_id:
            self.current_task_id = task_id
            self.setup_UI('selected')

    def on_task_double_clicked(self, index: QModelIndex):
        self.task_delegate.editing_index = index
        self.list_view.viewport().update()

    def open_context_menu(self, position: QPoint):
        pass
