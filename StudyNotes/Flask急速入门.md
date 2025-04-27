# Flask
Flask是一个微型后端框架

## 包下载
使用`pip install flask`下载

## Hello world



```python
from flask import Flask

# 创建Flask的实例 app对象
app = Flask(__name__)

# 使用装饰器绑定路由
@app.route('/')
def hello_world():
    return "hello world"

@app.route('/ciallo')
def ciallo():
    return "Ciallo～(∠・ω< )⌒★"

app.run()
```

该代码为flask的基础用法：

- 需要创建一个对象app，将flask框架实例化
- 使用装饰器绑定路由，route中的路径即为指定路由
  - 如`'/'`时，直接访问`http://127.0.0.1:5000`即可，但若为`'/index'`，我们需要访问`http://127.0.0.1:5000/index`才能获取到内容
  - 代码中定义了两个方法，每个都有对应绑定的路由，通过添加不同路由可以访问到对应内容
- 定义一个函数返回helloworld
- 使用`app.run()`运行，若在服务器上执行代码，需要添加`host='0.0.0.0'`表示允许任何主机访问

## 变量规则
在路由url中的一部分用变量代替，标记为`<变量类型:变量名>`，作为关键字传给与规则相关联的函数
支持变量类型如下：
| 类型| 说明|
| :-----: | :------: |
| string | 接受任何不含斜杠的文本（缺省值） |
| int | 接受正整数 | 
| float | 接受正浮点数 |
| path | 接受包含斜杠的字符串 |
| uuid | 接受uuid字符串 |


```python
from flask import Flask
from re import escape

app = Flask(__name__)

@app.route('/str/<username>')
def name(username):
    return "hello %s" % username

@app.route('/num/<int:number>')
def double(number):
    return "doubled = %s" % (number+number)

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'subpath: %s' % escape(subpath)

app.run()
```

## 唯一的URL与重定向行为
以下两条路由的不同在于是否使用尾部斜杠



```python
from flask import Flask

app = Flask(__name__)

@app.route('/projects/')
def projects():
    return 'the project page'

@app.route('/about')
def about():
    return 'the about page'

app.run()
```

`projects`中的url尾部有一个斜杠，表现同一个文件夹，在访问一个没有斜杠结尾的url时，flask回自动重定向，帮你加一个斜杠
`about`的url没有尾部斜杠，表现如同一个文件，若在访问时加了尾部斜杠会得到404错误
**尽量使用后者的写法，因为可以保持url唯一，避免搜索引擎重复索引同一页面**

## Flask重定向
访问某个网站时跳到另一个页面获取资源的方法
需要导入redirect函数，在括号中添加需要的页面


```python
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/redirect')
def redi():
    return redirect('https://izayoisakuye.github.io/')

app.run()
```

## JSON接口
每个路由接口可以自定GET方法（默认）或POST方法
我们使用POSTMAN来处理POST
获取的数据可以以json, xml, form等方式记录，我们这里使用json


```python

from flask import Flask, request, jsonify
from re import escape

app = Flask(__name__)

@app.route('/test/post', methods=["POST"])
def post():
    try:
        my_json = request.get_json()
        print(my_json)
        get_name = my_json.get("name")
        get_age = my_json.get("age")
        if not all([get_name, get_age]):
            return jsonify(msg="Insufficient parameters")
        get_age += 10
        return jsonify(name=get_name, age=get_age)
    except Exception as e:
        print(e)
        return jsonify(msg="error")

app.run()
```

- 该route调用了POST方法，故只能通过POST调用
- 以json处理时可以导入`jsonify`来返回json格式的数据
- 使用`try exception`使出错时的显示更加合理

## Flask Cookies
若要访问cookies，可以使用cookies属性
`set_cookies`方法可以设置cookies
请求对象的cookies是一个包含了客户端传输的所有cookies的字典
**Flask中使用session比cookies更安全**



```python
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

# 读取cookies
@app.route('/')
def index():
    username = request.cookies.get('username')

# 储存cookies
@app.route('/')
def restore():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
```
