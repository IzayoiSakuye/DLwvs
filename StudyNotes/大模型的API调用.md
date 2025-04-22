# 大模型的API调用 

## 什么是API：
    API是应用程序编程接口，通过定义的一套规则，使得不同软件系统间能相互通信，帮助一个程序向另一个请求数据或功能
    而大模型的API是为大型**预训练**模型提供的应用程序编程接口，通过API，开发者可以在自己的应用程序中整合和使用这些大模型的功能，而不用自己训练模型
    如ChatGPT之类的大模型，通过API对外提供服务，用户可以通过发送特定请求，获取模型对文本、图像等数据的理解和处理结果

## 为什么要选择调用API：
- 节省资源：不需要购买和维护昂贵的服务器硬件，也不需要花费时间和计算资源来训练模型。
- 易于集成：API的使用方式通常是简单的HTTP请求，便于集成到各种应用中。
- 实时更新：模型通常由提供者维护和更新，用户可以不定期获得性能改进和功能扩展。
- 可扩展性：用户可以根据需要调整请求的数量和规模，以适应不同的业务需求。

## 如何获取API KEY
本项目使用**DeepSeek-R1**作为调用模型：
- 进入DeepSeek开放平台，充值
- 选择API Keys，创建API Key并保存

## 代码调用
根据DS官网接口文档，调用前需要升级OpenAI SDK
`pip3 install -U openai`
下面代码为推理模型访问思维链与回答代码


```python
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Round 2
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)
# ...

```

输入参数：
- `max_tokens`：最终回答的最大长度（不含思维链输出），默认为 4K，最大为 8K。请注意，思维链的输出最多可以达到 32K tokens.
输出字段：
- `reasoning_content`：思维链内容，与 content 同级.
- `content`：最终回答内容


```python

```
