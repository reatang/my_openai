

# openai 结构化输出示例
#
# 结构化输出的两种形式
# 1. 通过`json mode`输出 - 使用prompt的描述
# 2. 通过结构化输出特性
#    - JSON Schema
#         - pydantic 模型定义
#         - 手动定义
#    - Function calling
# 参考：https://zhuanlan.zhihu.com/p/21986473257

import os
from typing import List

import rich
from pydantic import BaseModel

from openai import OpenAI, pydantic_function_tool
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["HUNYUAN_API_KEY"],
    base_url="https://api.hunyuan.cloud.tencent.com/v1",
)


# 使用json mode输出
def json_structured_output():
    system_prompt = """
    The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

    EXAMPLE INPUT: 
    Which is the highest mountain in the world? Mount Everest.

    EXAMPLE JSON OUTPUT:
    {
        "question": "Which is the highest mountain in the world?",
        "answer": "Mount Everest"
    }
    """
    completion = client.beta.chat.completions.parse(
        model="hunyuan-large",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请帮我得出解： 8x + 31 = 2"},
        ],
    )

    message = completion.choices[0].message
    rich.print(message)

# 使用 tool_calls

class Query(BaseModel):
    class_id: int
    student_id: int

class WebSearch(BaseModel):
    """
    Search the web for information.
    """
    search: str

def tool_calls_output():
    system_prompt = """你是一个结构化输出的工具. 请为工具`query`解析输入内容中的关键参数."""

    # 注意 结构化输出 `parse`
    completion = client.beta.chat.completions.parse(
        model="hunyuan-large",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请帮我查询班级134123中学生123123的信息."},
        ],
        tools=[
            # 据测试 pydantic_function_tool 仅用于结构化输出的tool_calls，真实的功能型 tool_calls 仅用于描述工具的入参
            pydantic_function_tool(Query, name="query", description="查询学生在班级中的信息."),
            pydantic_function_tool(WebSearch, name="web_search")
        ]
    )

    message = completion.choices[0].message
    rich.print(message)
    

# 使用结构化输出特性
class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

def structured_output():
    completion = client.beta.chat.completions.parse(
        model="hunyuan-large",
        messages=[
            {"role": "system", "content": "你是一个专业的数学博士."},
            {"role": "user", "content": "请帮我得出解： 8x + 31 = 2"},
        ],
        response_format=MathResponse,
    )

    message = completion.choices[0].message
    if message.parsed:
        rich.print(message.parsed.steps)

        print("answer: ", message.parsed.final_answer)
    else:
        print(message.refusal)

if __name__ == "__main__":

    # 使用json mode输出
    # 结论：混元支持json mode输出
    # json_structured_output()

    # 使用tool_calls
    # 结论：混元支持tool_calls
    tool_calls_output()

    # 使用结构化输出特性
    # 结论：混元不支持结构化输出
    # structured_output()
