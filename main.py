from taskdb import TaskManager, Priority

if __name__ == "__main__":
   # 创建任务管理器实例
   task_manager = TaskManager()

   # 初始化数据库
   # task_manager.initialize_database()

   # 添加任务并获取任务ID
   task_id = task_manager.add_task('Finish project', Priority.HIGH, '2024-06-30 18:00')
   print(f"Added Task ID: {task_id}")

   # 获取并打印所有任务
   tasks = task_manager.get_tasks()
   for task in tasks:
      print(task)

   # 更新任务
   task_manager.update_task(task_id, 'Finish project update', Priority.MEDIUM, '2024-07-01 18:00')

   # 打开任务解释文件
   task_manager.open_description_file(task_id)

   # 删除任务
   task_manager.delete_task(task_id)