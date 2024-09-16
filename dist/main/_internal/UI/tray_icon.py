from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon, QColor
from .config import ICON_PATH, MENU_STYLE_PATH


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(QIcon(ICON_PATH), parent)

        # 创建托盘菜单
        self.tray_menu = QMenu(parent)

        self.info_action = QAction("taskZen 2.0", parent)
        self.info_action.setEnabled(False)
        self.tray_menu.addAction(self.info_action)

        # 添加显示主界面的动作
        self.show_action = QAction("显示主界面", parent)
        self.show_action.triggered.connect(self.show_main_window)
        self.tray_menu.addAction(self.show_action)

        # 添加隐藏主界面的动作
        self.hide_action = QAction("隐藏主界面", parent)
        self.hide_action.triggered.connect(self.hide_main_window)
        self.tray_menu.addAction(self.hide_action)

        # 添加退出应用程序的动作
        self.quit_action = QAction("关闭软件", parent)
        self.quit_action.triggered.connect(self.quit)
        self.tray_menu.addAction(self.quit_action)

        # 设置托盘图标的菜单
        self.setContextMenu(self.tray_menu)

        # 显示托盘图标
        self.show()

        # 连接托盘图标的激活事件
        self.activated.connect(self.event_filter)

        # 设置右键菜单展示或隐藏
        self.update_menu()

        # 应用样式表
        self.load_stylesheet()

    def load_stylesheet(self):
        style_file = QFile(MENU_STYLE_PATH)
        style_file.open(QFile.ReadOnly)
        self.tray_menu.setStyleSheet(style_file.readAll().data().decode())
        self.tray_menu.setWindowFlag(Qt.FramelessWindowHint)
        self.tray_menu.setWindowFlag(Qt.NoDropShadowWindowHint)
        self.tray_menu.setAttribute(Qt.WA_TranslucentBackground)

    def event_filter(self, event):
        if event == QSystemTrayIcon.Trigger:
            if self.parent().isVisible():
                self.parent().hide()
            else:
                self.parent().show()
        self.update_menu()

    def show_main_window(self):
        self.parent().show()
        self.update_menu()

    def hide_main_window(self):
        self.parent().hide()
        self.update_menu()

    def quit(self):
        self.parent().quit()

    def update_menu(self):
        if self.parent().isVisible():
            self.show_action.setVisible(False)
            self.hide_action.setVisible(True)
        else:
            self.show_action.setVisible(True)
            self.hide_action.setVisible(False)
