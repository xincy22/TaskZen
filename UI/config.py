import os

UI_DIR = os.path.dirname(os.path.abspath(__file__))

# style文件
MAIN_WINDOW_STYLE_PATH = os.path.join(UI_DIR, 'style', 'mainwindow.css')
INPUT_WINDOW_STYLE_PATH = os.path.join(UI_DIR, 'style', 'inputwindow.css')
TASKITEM_STYLE_PATH = os.path.join(UI_DIR, 'style', 'taskitem.css')

# 字体
FONT_PATH = os.path.join(UI_DIR, 'style', 'LXGWWenKaiLite-Regular.ttf')