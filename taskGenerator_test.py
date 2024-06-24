from chat import TaskGenerator

def main():
    # 创建 TaskGenerator 实例
    task_generator = TaskGenerator()

    # 测试用户输入
    user_inputs = [
        "我需要在下周五之前完成一份市场分析报告，这个任务非常重要。",
        "请帮我在明天中午12点之前准备好会议材料，这个任务比较紧急。",
        "下个月初之前完成年度总结报告，这个任务一般。"
    ]

    # 生成任务信息并打印结果
    for user_input in user_inputs:
        task_info = task_generator.generate(user_input)
        print(f"用户输入: {user_input}")
        print(f"生成的任务信息: {task_info}\n")

if __name__ == "__main__":
    main()