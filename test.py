from chat import task_generator
import time

start_time = time.time()
print(task_generator.chat("""
我需要在今天晚上完成智能电子产品创新实践的作业
"""))
end_time = time.time()
print(f"运行时间：{end_time - start_time}s")