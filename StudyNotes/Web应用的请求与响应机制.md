# Web应用的请求与响应机制
## HTTP协议

HTTP是web通信的基础协议，是客户端与服务器进行交互的标准，所有www文件必须遵守这个标准，**其端口号为80**

HTTPS是HTTP的安全版，在HTTP下加入SSL层
SSL是主要用于web的安全传输协议，在传输层对网络连接进行加密，**其端口号为443**


### 工作原理
HTTP通信由两部分组成：客户端请求信息、服务器响应信息
- 当用户在地址栏输入一个URL并回车后，客户端向web服务器发送HTTP请求，建立一个到服务器指定端口的TCP连接
- 服务器在那个端口监听客户端发送过来的请求，收到请求后，服务器根据内容与类型进行处理，并生成HTTP响应，包括一个状态行与相应的信息
- 客户端接受服务器返回的响应，并根据内容呈现给用户

### URL
统一资源定位符（Uniform / Universal Resource Locator），是用于完整描述网页和其他资源的地址的一种标识方法
**基本格式： `scheme://host[:port#]/path/…/[?query-string][#anchor]`**
- scheme：协议（如http与https）
- host：服务器ip地址或域名
- port：服务器端口（如果走协议默认端口，缺省端口80）
- path：访问资源的路径
- query-string：参数，发送给http服务器的数据
- anchor：锚，跳转到网页的指定锚点位置

### HTTP请求
HTTP用来提交和获取资源，客户端发送一个HTTP请求请求到服务器的请求信息，包括：请求行、请求头部、空行、请求数据四个部分，格式如下

![HTTP请求](https://i-blog.csdnimg.cn/blog_migrate/925eb592741c87dae2107c846ddb5aba.png)

一些常用的请求报头：
- Host：对应URL中的web名称与端口号，用于指定被请求资源的Internet主机与端口号
- Connection：表示客户端与服务器连接类型
    Client 发起一个包含 Connection:keep-alive 的请求， HTTP/1.1 使用 keep-alive 为默认值。
    Server 收到请求后：如果 Server 支持 keep-alive（长连接）， 回复一个包含 Connection:keep-alive 的响应， 不关闭连接；如果 Server 不支持 keep-alive， 回复一个包含 Connection:close 的响应， 关闭连接。如果 client 收到包含 Connection:keep-alive 的响应， 向同一个连接发送下一个请求， 直到一方主动关闭连接。
    keep-alive 在很多情况下能够重用连接， 减少资源消耗， 缩短响应时间， 比如当浏览器需要多个文件时(比如一个 HTML 文件和相关的图形文件)， 不需要每次都去请求建立连接。
- Upgrade-Insecure-Requests：升级不安全的请求， 意思是会在加载 http 资源时自动替换成 https 请求， 让浏览器不再显示 https 页面中的 http 请求警报。
- User-Agent：客户浏览器的详细信息，服务器根据这条信息来判断来访用户是否为真实用户
- Accept：指浏览器或其他客户端可以接受的MIME（Multipurpose Internet Mail Extensions）文件类型，服务器根据其判断并返回适当文件格式
  - Accept: /： 表示什么都可以接收。
  - Accept: text/html, application/xhtml+xml;q=0.9, image/*;q=0.8：
    表示浏览器支持的 MIME 类型分别是html文本、xhtml和xml文档、 所有的图像格式资源。
    q是权重系数， 范围 $0 =< q <= 1$，q值越大，请求越倾向于获得其“;”之前的类型表示的内容。若没有指定 q 值， 则默认为1，按从左到右排序顺序；若被赋值为 0，则用于表示浏览器不接受此内容类型。
    Text：用于标准化地表示的文本信息，文本消息可以是多种字符集和或者多种格式的；
    Application：用于传输应用程序数据或者二进制数据。
  - Referer：表明产生请求的网页来自于哪个URL，用户是从该referer页面访问到当前请求的页面，可以用来跟踪web请求来自哪个页面，哪个网站
  - Accept-Encoding：指出浏览器可以接受的编码方式。 编码方式不同于文件格式， 它是为了压缩文件并加速文件传递速度。 浏览器在接收到 Web 响应之后先解码， 然后再检查文件格式， 许多情形下这可以减少大量的下载时间。
    如Accept-Encoding:gzip;q=1.0, identity; q=0.5, *;q=0
    如果有多个 Encoding 同时匹配, 按照q值顺序排列，本例中按顺序支持 gzip, identity压缩编码， 支持gzip的浏览器会返回经过gzip编码的HTML页面。 如果请求消息中没有设置这个域服务器假定客户端对各种内容编码都可以接受。
  - Accept-Language：指语言可以接受的语言种类，如zh或zh-cn指中文
  - Accept-Charset：指浏览器可以接受的字符编码，缺省为任何字符集
  - Cookie：浏览器用这个属性向服务器发送 Cookie。
  - Content-Type：POST请求里用来表示的内容类型。

示例：

![HTTP请求示例](https://i-blog.csdnimg.cn/blog_migrate/21c6fd7651fd37a38c96cdaebb1ba542.png)

### 常见HTTP方法

- GET：请求指定资源，通常附加在URL中，不适合传递大量数据与隐私数据

- POST：向服务器提交数据，通常用于提交表单与上传文件

- PUT：更新指定资源内容

- HEAD：只返回响应头，不返回响应体

- OPTIONS：查询服务器支持的HTTP方法

  
### HTTP响应
由四部分组成，分别为状态行、消息报头、空行、响应正文，格式如下：

![HTTP响应](https://i-blog.csdnimg.cn/blog_migrate/8c9e4d37f17a3b0e3706e5d10b280aa2.png)

理论上所有响应头信息都是回应请求头的，但还会添加对应的响应头信息

示例：

![HTTP响应示例](https://i-blog.csdnimg.cn/blog_migrate/ec31faa6f61a7d1a6c7495c60608eff2.png)

### HTTP状态码

web服务器对HTTP请求的回应，表示请求是否成功处理

- 1xx：服务器成功接受部分请求
- 2xx：成功（200 OK）
- 3xx：重定向（301 Moved Permanently）
- 4xx：客户端错误（404 Not Found）
- 5xx：服务器错误（500 Internal Server Error）

### Cookie与Session：
服务器和客户端的交互仅限于请求/响应过程，结束之后便断开，在下一次请求时，服务器会认为新的客户端。为了维护他们之间的链接，让服务器知道这是前一个用户发送的请求，必须在一个地方保存客户端的信息。
- Cookie：通过在 客户端 记录的信息确定用户的身份。
- Session：通过在 服务器端 记录的信息确定用户的身份



## 请求参数的获取与处理

HTTP携带多种数据，这里通过python，使用urllib与requests库来处理这些数据

### 处理URL路径与查询参数

​	URL 查询参数是指在 URL 中通过键值对的形式传递的参数，用于在 URL 中增加额外的信息，如查询条件、排序方式、页码等。查询参数通常使用键值对的形式定义，键和值之间用 = 符号分隔，多个参数之间用 & 符号分隔。例如，定义一个查询参数 page 的值为 *2*，可以写成 page=2

​	查询参数的主要用途是通过 URL 传递信息，实现搜索查询、过滤器等功能。例如，用户在输入框输入 *abc*，按下回车之后，会返回一条地址为 *https://www.example.com/?keyword=abc* 的 URL。在用户访问时，服务器会通过 URL 参数 keyword 检索相关内容，然后返回给用户

​	在python中，可以使用urllib库中urllib.parse模块中的`parse_qs`函数来解析查询字符串，以下为示例程序，程序返回字典，键值对分别为等号左右的内容


```python
from urllib.parse import urlparse, parse_qs

# 示例URL
url = 'http://example.com/path/to/resource?name=John&age=30'

# 解析URL
parsed_url = urlparse(url)

# 获取路径
path = parsed_url.path
print("Path:", path)

# 解析查询参数
query_params = parse_qs(parsed_url.query)
print("Query Parameters:", query_params)
```

    Path: /path/to/resource
    Query Parameters: {'name': ['John'], 'age': ['30']}


### 处理表单数据
    表单数据是通过网页上的表单收集并提交给服务器的信息，用户可以填写表单来提供各种信息。当用户点击表单上的提交按钮时，表单数据会被发送到服务器，服务器则根据接收到的数据执行相应操作
    表单的基本结构如下
    ```html
    <form action="/submit" method="post">
        <label for="username">用户名:</label>
        <input type="text" id="username" name="username"><br><br>
        
        <label for="password">密码:</label>
        <input type="password" id="password" name="password"><br><br>
        
        <input type="submit" value="提交">
    </form>
    ```
`<form>`标签定义了一个表单，action属性指定了表单数据提交的目标url，method属性制定了提交数据时使用的HTTP方法
- GET：当method属性被设置为GET时，表单数据会被附加在url后面作为查询参数提交。这种方法适合提交少量的非敏感数据
- POST：当method属性被设置为POST时，表单数据会在请求体中发送，不会出现在url中。这种方法适合提交敏感与大量数据
  `<input>`标签用于创建输入控件，type属性定义了输入控件的类型，name属性为提交属性时的键名，id用于关联`<label>`标签
  `<label>`标签用于描述每个输入控件的用途
    表单数据的编码：
- application/x-www-form-urlencoded：这是默认的编码方式，表单数据被编码成键值对的形式，如 username=John&password=Doe。
- multipart/form-data：当表单中包含文件上传字段时，必须使用此编码方式。它允许将文件和其他数据一起发送。

我们可以在python中通过request库发送POST请求来获取表单数据并处理，返回的是html类型的表单数据


```python
import requests

# 示例表单数据
form_data = {
    'username': 'john_doe',
    'password': 'securepassword'
}

# 发送POST请求
response = requests.post('https://www.baidu.com/', data=form_data)

# 查看响应
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)
```



    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <title>é¡µé¢ä¸å­å¨_ç¾åº¦æç´¢</title>

​    


### 处理JSON数据
python中可以使用request库来处理json数据


```python
import requests
import json

# 示例JSON数据
json_data = {
    'name': 'John',
    'age': 30
}

# 发送POST请求
response = requests.post('https://www.baidu.com/', json=json_data)

# 查看响应
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
```

    Response Status Code: 302



    ---------------------------------------------------------------------------
    
    JSONDecodeError                           Traceback (most recent call last)
    
    File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\models.py:971, in Response.json(self, **kwargs)
        970 try:
    --> 971     return complexjson.loads(self.text, **kwargs)
        972 except JSONDecodeError as e:
        973     # Catch JSON-related errors and raise as requests.JSONDecodeError
        974     # This aliases json.JSONDecodeError and simplejson.JSONDecodeError


    File ~\AppData\Local\Programs\Python\Python312\Lib\json\__init__.py:346, in loads(s, cls, object_hook, parse_float, parse_int, parse_constant, object_pairs_hook, **kw)
        343 if (cls is None and object_hook is None and
        344         parse_int is None and parse_float is None and
        345         parse_constant is None and object_pairs_hook is None and not kw):
    --> 346     return _default_decoder.decode(s)
        347 if cls is None:


    File ~\AppData\Local\Programs\Python\Python312\Lib\json\decoder.py:337, in JSONDecoder.decode(self, s, _w)
        333 """Return the Python representation of ``s`` (a ``str`` instance
        334 containing a JSON document).
        335 
        336 """
    --> 337 obj, end = self.raw_decode(s, idx=_w(s, 0).end())
        338 end = _w(s, end).end()


    File ~\AppData\Local\Programs\Python\Python312\Lib\json\decoder.py:355, in JSONDecoder.raw_decode(self, s, idx)
        354 except StopIteration as err:
    --> 355     raise JSONDecodeError("Expecting value", s, err.value) from None
        356 return obj, end


    JSONDecodeError: Expecting value: line 1 column 1 (char 0)


​    
​    During handling of the above exception, another exception occurred:


    JSONDecodeError                           Traceback (most recent call last)
    
    Cell In[5], line 15
         13 # 查看响应
         14 print("Response Status Code:", response.status_code)
    ---> 15 print("Response JSON:", response.json())


    File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\models.py:975, in Response.json(self, **kwargs)
        971     return complexjson.loads(self.text, **kwargs)
        972 except JSONDecodeError as e:
        973     # Catch JSON-related errors and raise as requests.JSONDecodeError
        974     # This aliases json.JSONDecodeError and simplejson.JSONDecodeError
    --> 975     raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)




### 处理文件上传
    HTTP文件上传是通过HTTP协议将文件从客户端传输到服务器的一种方式。通常使用POST方法，并且数据格式为multipart/form-data。这种格式允许在同一个请求中传输多个字段和文件。
    HTTP文件上传中，请求头需要包含Content-Type，其值为multipart/form-data，并指定一个边界（boundary），用于分隔不同的字段和文件。例如
    ```html
    POST /upload HTTP/1.1
    Host: www.example.com
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundarycz5DOEJKqu7XXB7k
    
    ------WebKitFormBoundarycz5DOEJKqu7XXB7k
    Content-Disposition: form-data; name="file"; filename="example.png"
    Content-Type: image/png
    
    <文件内容>
    ------WebKitFormBoundarycz5DOEJKqu7XXB7k--
    ```
    我们可以使用python的request库来处理文件上传响应


```python
import requests

# 打开文件
files = {'file': open('example.txt', 'rb')}

# 发送POST请求
response = requests.post('http://example.com/upload', files=files)

# 查看响应
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)
```


    ---------------------------------------------------------------------------
    
    FileNotFoundError                         Traceback (most recent call last)
    
    Cell In[6], line 4
          1 import requests
          3 # 打开文件
    ----> 4 files = {'file': open('example.txt', 'rb')}
          6 # 发送POST请求
          7 response = requests.post('http://example.com/upload', files=files)


    File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\IPython\core\interactiveshell.py:325, in _modified_open(file, *args, **kwargs)
        318 if file in {0, 1, 2}:
        319     raise ValueError(
        320         f"IPython won't let you open fd={file} by default "
        321         "as it is likely to crash IPython. If you know what you are doing, "
        322         "you can use builtins' open."
        323     )
    --> 325 return io_open(file, *args, **kwargs)


    FileNotFoundError: [Errno 2] No such file or directory: 'example.txt'



```python

```
