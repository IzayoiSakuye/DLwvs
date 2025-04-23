from openai import OpenAI

# 输入API与URL
client = OpenAI(
    api_key="***REMOVED***",
    base_url="https://api.deepseek.com"
)


web_URL = input("请输入待检测的链接:")
# # 读取文件中对应的请求与响应数据
# with open('input_request.txt', 'r') as file:
#     web_request = file.read()
#
# with open('input_response.txt', 'r') as file:
#     web_response = file.read()
'''
构造prompt，让大模型协助判断漏洞
注意：prompt分为两部分
- 角色设定：指定ai所担任的角色为Web安全专家，使得回复有更合适的风格
- 输入内容：输入待测链接，使用格式化代替输入
- 
'''
prompt = f"""
你是一个Web安全专家。请你根据下面的链接判断是否存在Web安全漏洞，并指出漏洞类型与原因。

链接：
{web_URL}

请详细说明你是如何判断的，并给出**最有可能**的结论以及测试方法，以格式
测试方法：
预期漏洞：
输出

若没有明显的漏洞特征，允许得到**正常**的结论
"""

# 发送请求
messages = [{"role": "user", "content": prompt}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

# 获取大模型的回答
reasoning = getattr(response.choices[0].message, "reasoning_content", "无详细推理")
answer = response.choices[0].message.content

# 将结果输出至文件
with open('output_reasoning.txt', 'w') as file:
    file.write(reasoning)
with open('output_answer.txt', 'w') as file:
    file.write(answer)
print("结果已生成")
# print("推理过程：\n", reasoning)
# print("\n检测结果：\n", answer)
