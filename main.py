import sys
from PyQt5.QtWidgets import QApplication
from taskUI import TaskManagerUI
from chat import QwenModel



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = TaskManagerUI()
    ui.show()
    sys.exit(app.exec_())