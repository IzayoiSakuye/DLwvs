from openai import OpenAI

# 输入API与URL
client = OpenAI(
    api_key="***REMOVED***",
    base_url="https://api.deepseek.com"
)

# 对应的请求与响应数据
web_request = """GET /search.php?q=1' OR '1'='1 HTTP/1.1
Host: vulnerable-website.com
User-Agent: Mozilla/5.0
"""

web_response = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<title>Search Results</title>
You have an error in your SQL syntax
</html>
"""

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

print("推理过程：\n", reasoning)
print("\n检测结果：\n", answer)
