import openai
import os
import json
import rich
from dotenv import load_dotenv

from my_openai import tool_map, openai_tool_calls

# 加载 .env 文件中的环境变量
load_dotenv()

client = openai.OpenAI(
    api_key=os.environ["HUNYUAN_API_KEY"],
    base_url="https://api.hunyuan.cloud.tencent.com/v1",
)

def run_agent(prompt):
    """
    使用 OpenAI API 运行 Hunyuan 代理。
    """

    messages = [
        {"role": "system", "content": "你是一名助教，通过调用工具函数来帮助我回答问题。无前后依赖工具可以并发调用。"},
        {"role": "user", "content": prompt},
    ]

    # 一个带tool_calls
    for i in range(20):
        # 使用 OpenAI API 运行 Hunyuan 代理
        chat_completion = client.chat.completions.create(
            model="hunyuan-large", # <- 使用 Hunyuan 大模型
            messages=messages,
            tools=openai_tool_calls,
            extra_body={
                # "enable_enhancement": True, # <- 自定义参数
            },
        )

        rich.print(chat_completion)

        choice = chat_completion.choices[0]

        # 检测tool_calls
        if not choice.message.tool_calls:
            return choice.message.content

        messages.append(choice.message)
        for tool_call in choice.message.tool_calls: # <-- tool_calls 可能是多个，因此我们使用循环逐个执行
            
            if isinstance(tool_call, openai.types.chat.ChatCompletionMessageToolCall):
                # ChatCompletionMessage 格式的 tool_call 包含了函数的名称和参数
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(tool_call.function.arguments) # <-- arguments 是序列化后的 JSON Object，我们需要使用 json.loads 反序列化一下
                tool_function = tool_map[tool_call_name] # <-- 通过 tool_map 快速找到需要执行哪个函数
                tool_result = tool_function(**tool_call_arguments)
            else:
                raise ValueError(f"Unknown tool call type: {type(tool_call)}")
    
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_name,
                "content": json.dumps(tool_result), 
            })

if __name__ == "__main__":
    # 示例用法
    prompt = "查询所有课程的所有学生名称。"
    generated_text = run_agent(prompt)
    print(f"Prompt: {prompt}")
    print(f"Generated Text: {generated_text}")
