# main.py
from chat import QwenModel

def main():
    # 创建 QwenModel 实例
    qwen_model = QwenModel()

    # 测试提示文本
    prompt = "Tell me a joke."

    # 生成响应文本
    response = qwen_model.generate(prompt)

    # 打印响应文本
    print("Prompt:", prompt)
    print("Response:", response)

if __name__ == "__main__":
    main()