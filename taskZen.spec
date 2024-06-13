# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # 主脚本
    pathex=['.'],  # 搜索路径
    binaries=[],
    datas=[
        ('styles/styles.qss', 'styles'),  # 样式表
        ('styles/taskZen.ico', 'styles'),  # 图标
        ('config.py', '.'),  # 配置文件
        ('LICENSE', '.'),  # 许可证文件
        ('descriptions', 'descriptions'),  # 描述文件夹
        ('notifier', 'notifier'),  # notifier 文件夹
        ('taskdb', 'taskdb'),  # taskdb 文件夹
        ('taskUI', 'taskUI')  # taskUI 文件夹
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='taskZen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 如果你希望看到控制台输出，可以将其设置为True
    icon='styles/taskZen.ico',  # 设置图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='taskZen',
)