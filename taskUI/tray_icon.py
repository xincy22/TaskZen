from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(QIcon("taskZen.ico"), parent)
        
        # Create tray menu
        tray_menu = QMenu(parent)
        
        show_action = QAction("Show", parent)
        show_action.triggered.connect(parent.show)
        
        hide_action = QAction("Hide", parent)
        hide_action.triggered.connect(parent.hide)
        
        quit_action = QAction("Quit", parent)
        quit_action.triggered.connect(parent.close)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        
        self.setContextMenu(tray_menu)
        
        # Show tray icon
        self.show()