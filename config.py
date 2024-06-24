import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库文件路径
DATABASE_PATH = os.path.join(BASE_DIR, 'taskdb', 'tasks.db')

# 任务解释文件路径
DESCRIPTION_DIR = os.path.join(BASE_DIR, 'descriptions')

# 图标途径
ICON_PATH = os.path.join(BASE_DIR, 'styles', 'taskZen.ico')

# 样式文件路径
STYLE_PATH = os.path.join(BASE_DIR, 'styles', 'styles.qss')

# 确保描述文件目录存在
os.makedirs(DESCRIPTION_DIR, exist_ok=True)

# 模型缓存目录
MODEL_CACHE_DIR = os.path.join(BASE_DIR, 'model_cache')
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)