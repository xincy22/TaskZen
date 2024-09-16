import sys
from UI import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat
import taskdb

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
