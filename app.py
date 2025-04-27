from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory
import re # 正则表达式

# 输入API与URL
client = OpenAI(
    api_key="***REMOVED***",
    base_url="https://api.deepseek.com"
)

# 创建flask应用实例
app = Flask(__name__, static_folder='./web', static_url_path='/')

@app.route('/')
# 本地部署网页
def index():
    return send_from_directory(app.static_folder, 'index.html')

# 使用装饰器定义路由，并限定接受POST方法
@app.route('/api/detect', methods=['POST'])
# 定义一个函数，用于调用大模型api检测漏洞
def detect_vulnerability():
    # 获取前端的json数据
    data = request.get_json()
    # 提取出url参数
    url = data.get('url','')
    # 判断输入的url是否合理
    if not url.startswith(('http://', 'https://')):
        return jsonify({'vul': '无效的url格式', 'method':'无效的url格式'}), 400

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
    {url}

    请详细说明你是如何判断的，并给出**最有可能**的结论以及测试方法，以格式
    预期漏洞：
    测试方法：
    输出，并且使用纯文本格式，不需要markdown语法
    若均没有明显的漏洞特征，允许得到**正常**的结论
    """
    # 请求大模型API
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages
    )
    # 获取回答
    reasoning = getattr(response.choices[0].message, "reasoning_content", "无详细推理")
    answer = response.choices[0].message.content
    return jsonify(dist_answer(answer))

# 从大模型生成的回答中提取预期漏洞与测试方法信息
def dist_answer(text):
    # 使用正则表达式测试
    vul = re.search(r'预期漏洞：\s*(.+?)(\n|$)', text)
    method = re.search(r'测试方法：\s*(.+?)(\n\n|$)', text, re.DOTALL)

    return {
        'method': method.group(1).strip().replace('\n', '<br>') if method else '无',
        'vul': vul.group(1).strip().replace('\n', '<br>') if vul else '可能无漏洞'
    }

app.run()
