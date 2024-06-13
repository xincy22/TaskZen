import sys
from PyQt5.QtWidgets import QApplication
from taskUI import TaskManagerUI

def main():
    app = QApplication(sys.argv)
    ex = TaskManagerUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()