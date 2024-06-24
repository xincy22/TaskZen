from .model import ChatGLMClient
from datetime import datetime, timedelta

now = datetime.now()
tonight = now.replace(hour=23, minute=59, second=59)
tomorrow = tonight + timedelta(days=1)
next_monday = tonight + timedelta(days=(7 - now.weekday()))

task_generator = ChatGLMClient()
task_generator.set_system_prompt(f"""
### Prompt

请根据以下用户的自然语言输入生成一个包含任务信息的JSON数据。任务信息包括以下字段：
- 任务名称 (task_name)
- 任务紧急程度 (priority)，其值必须是 "高"、"中" 或 "低"
- 任务截止时间 (due_date)

注意当前的时间为{now.strftime("%Y-%m-%d %H:%M:%S")}，你可能需要结合当前时间推断用户任务的截止时间`due_date`
### 用户输入示例

用户输入: 我明天需要完成实验报告

### 示例输出

```json
{{
  "task_name": "完成实验报告",
  "priority": "高",
  "due_date": {tomorrow.strftime("%Y-%m-%d %H:%M:%S")}
}}
```

### 更多用户输入示例

用户输入: 下周一之前提交项目计划书

### 示例输出

```json
{{
  "task_name": "提交项目计划书",
  "priority": "中",
  "due_date": {next_monday.strftime("%Y-%m-%d %H:%M:%S")}
}}
```

用户输入: 今天晚上完成代码调试

### 示例输出

```json
{{
  "task_name": "完成代码调试",
  "priority": "高",
  "due_date": {tonight.strftime("%Y-%m-%d %H:%M:%S")}
}}
```

### 注意事项
1. `priority` 字段的值必须是以下之一："高"、"中"、"低"。
2. `due_date` 字段应包含具体的日期和时间，格式为 "YYYY-MM-DD HH:MM:SS"。
3. 根据用户输入中的时间描述，合理推断 `due_date`。
""")