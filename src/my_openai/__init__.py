
from my_openai.tools import get_courses, get_course_info, get_student_info

tool_map = {
    "get_courses": get_courses,
    "get_course_info": get_course_info,
    "get_student_info": get_student_info,
}

openai_tool_calls = [
    {
		"type": "function", # 约定的字段 type，目前支持 function 作为值
		"function": { # 当 type 为 function 时，使用 function 字段定义具体的函数内容
			"name": "get_courses", # 函数的名称，请使用英文大小写字母、数据加上减号和下划线作为函数名称
			"description": """ 
				获取所有课程的信息。
			""", # 函数的介绍，在这里写上函数的具体作用以及使用场景，以便 Kimi 大模型能正确地选择使用哪些函数
			"parameters": {}
		}
	},
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": """ 
                获取指定课程的信息和学生的ID列表。
            """,
            "parameters": {
                "course_id": {
                    "type": "int",
                    "description": "课程的 ID。"
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_info",
            "description": """ 
                获取指定学生的信息。
            """,
            "parameters": {
                "student_id": {
                    "type": "int",
                    "description": "学生的 ID。"
                }
            }
        }
    }
]

__all__ = [
    "tool_map",
    "openai_tool_calls",
]