from openai import OpenAI

# 输入API与URL
client = OpenAI(
    api_key="***REMOVED***",
    base_url="https://api.deepseek.com"
)



# 读取文件中对应的请求与响应数据
with open('input_request.txt', 'r') as file:
    web_request = file.read()

with open('input_response.txt', 'r') as file:
    web_response = file.read()
'''
构造prompt，让大模型协助判断漏洞
'''
prompt = f"""
你是一个Web安全专家。请你根据下面的HTTP请求与响应内容判断是否存在Web安全漏洞，并指出漏洞类型与原因。

HTTP 请求内容：
{web_request}

HTTP 响应内容：
{web_response}

请详细说明你是如何判断的，并给出最有可能的结论。
若没有明显的漏洞特征，允许得到"正常"的结论
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

# print("推理过程：\n", reasoning)
# print("\n检测结果：\n", answer)
