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

    Response Status Code: 302
    Response Text: <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <style data-for="result" id="css_result">
    body{color:#333;background:#fff;padding:6px 0 0;margin:0;position:relative;min-width:900px}body,th,td,.p1,.p2{font-family:arial}p,form,ol,ul,li,dl,dt,dd,h3{margin:0;padding:0;list-style:none}input{padding-top:0;padding-bottom:0;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;box-sizing:border-box}table,img{border:0}td{font-size:9pt;line-height:18px}


​    
​    
    #foot{font-size:12px}.logo{width:117px;height:38px;cursor:pointer}
    
    #u,#head,#tool,#search,.p1{line-height:120%;margin-left:-12pt}.p2{width:100%;line-height:120%;margin-left:-12pt}#wrapper{_zoom:1}#container{word-break:break-all;word-wrap:break-word}.container_s{width:1002px}.container_l{width:1222px}#content_left{width:636px;float:left;padding-left:35px}#content_right{border-left:1px solid #e1e1e1;float:right}.container_s #content_right{width:271px}.container_l #content_right{width:434px}.content_none{padding-left:35px}#u{color:#999;white-space:nowrap;position:absolute;right:10px;top:4px;z-index:299}#u a{color:#00c;margin:0 5px}#u .reg{margin:0}#u .last{margin-right:0}#u .un{font-weight:bold;margin-right:5px}#u ul{width:100%;background:#fff;border:1px solid #9b9b9b}#u li{height:25px}#u li a{width:100%;height:25px;line-height:25px;display:block;text-align:left;text-decoration:none;text-indent:6px;margin:0;filter:none\9}#u li a:hover{background:#ebebeb}#u li.nl{border-top:1px solid #ebebeb}#user{position:relative;display:inline-block}#user_center{position:relative;display:inline-block}#user_center .user_center_btn{margin-right:5px}.userMenu{width:64px;position:absolute;right:7px;_right:2px;top:15px;top:14px\9;*top:15px;padding-top:4px;display:none;*background:#fff}#head{padding-left:35px;margin-bottom:20px;width:900px}
    
    .fm{clear:both;position:relative;z-index:297}.nv a,.nv b,.btn,#page,#more{font-size:14px}
    
    .s_nav{height:45px}.s_nav .s_logo{margin-right:20px;float:left}.s_nav .s_logo img{border:0;display:block}.s_tab{line-height:18px;padding:20px 0 0;float:left}.s_nav a{color:#00c;font-size:14px}.s_nav b{font-size:14px}.s_ipt_wr{width:536px;height:30px;display:inline-block;margin-right:5px;background-position:0 -96px;border:1px solid #b6b6b6;border-color:#7b7b7b #b6b6b6 #b6b6b6 #7b7b7b;vertical-align:top}.s_ipt{width:523px;height:22px;font:16px/22px arial;margin:5px 0 0 7px;padding:0;background:#fff;border:0;outline:0;-webkit-appearance:none}.s_btn{width:95px;height:32px;padding-top:2px\9;font-size:14px;padding:0;background-color:#ddd;background-position:0 -48px;border:0;cursor:pointer}.s_btn_h{background-position:-240px -48px}.s_btn_wr{width:97px;height:34px;display:inline-block;background-position:-120px -48px;*position:relative;z-index:0;vertical-align:top}.sethf{padding:0;margin:0;font-size:14px}.set_h{display:none;behavior:url(#default#homepage)}.set_f{display:none}.shouji{margin-left:19px}.shouji a{text-decoration:none}.bdsug{position:absolute;width:536px;background:#fff;display:none;border:1px solid #817f82}


​    
    #page{font:14px arial;white-space:nowrap;padding-left:35px}#page a,#page strong{display:inline-block;vertical-align:text-bottom;height:66px;text-align:center;line-height:34px;text-decoration:none;overflow:hidden;margin-right:9px;background:white}#page a{cursor:pointer}#page a:hover{background:0}#page .n:hover,#page a:hover .pc{background:#f2f8ff;border:1px solid #38f}#page .n{height:34px;padding:0 18px;border:1px solid #e1e2e3}#page span{display:block}#page .pc{width:34px;height:34px;border:1px solid #e1e2e3;cursor:pointer}#page .fk{width:24px;height:24px;margin-bottom:6px;margin-left:6px;cursor:pointer}#page strong .fk,#page strong .pc{cursor:auto}#page .fk .c-icon-bear-pn{top:-3px;position:relative}#page .fkd .c-icon-bear-pn{top:3px;position:relative}#page .fk_cur .c-icon-bear-p{top:-2px;position:relative}#page strong .pc{border:0;width:36px;height:36px;line-height:36px}#page .nums{display:inline-block;vertical-align:text-bottom;height:36px;line-height:36px;margin-left:10px}#rs{width:900px;background:#fff;padding:8px 0;margin:20px 0 0 15px}#rs td{width:5%}#rs th{font-size:14px;font-weight:normal;line-height:19px;white-space:nowrap;text-align:left;vertical-align:top}#rs .tt{font-weight:bold;padding:0 10px 0 20px}#rs_top{font-size:14px;margin-bottom:22px}#rs_top a{margin-right:18px}#search{width:900px;padding:35px 0 16px 35px}#search .s_help{position:relative;top:10px}
    
    #foot{height:20px;line-height:20px;color:#77c;background:#e6e6e6;text-align:center}#foot span{color:#666}
    
    .to_zhidao,.to_tieba,.to_zhidao_bottom{font-size:16px;line-height:24px;margin:20px 0 0 35px}.to_tieba .c-icon-tieba{float:left}.f{line-height:115%;*line-height:120%;font-size:100%;width:33.7em;word-break:break-all;word-wrap:break-word}.h{margin-left:8px;width:100%}.r{word-break:break-all;cursor:hand;width:238px}.t{font-weight:normal;font-size:medium;margin-bottom:1px}.pl{padding-left:3px;height:8px;padding-right:2px;font-size:14px}.mo,a.mo:link,a.mo:visited{color:#666;font-size:100%;line-height:10px}.htb{margin-bottom:5px}.jc a{color:#c00}a font[size="3"] font,font[size="3"] a font{text-decoration:underline}div.blog,div.bbs{color:#707070;padding-top:2px;font-size:13px}.result{width:33.7em;table-layout:fixed}.result-op .f{word-wrap:normal}.nums{font-size:12px;color:#999}.tools{position:absolute;top:10px;white-space:nowrap}
    
    #mHolder{width:62px;position:relative;z-index:296;top:-18px;margin-left:9px;margin-right:-12px;display:none}#mCon{height:18px;position:absolute;top:3px;top:6px\9;cursor:pointer;line-height:18px}.wrapper_l #mCon{right:7px}#mCon span{color:#00c;cursor:default;display:block}#mCon .hw{text-decoration:underline;cursor:pointer;display:inline-block}#mCon .pinyin{display:inline-block}#mCon .c-icon-chevron-unfold2{margin-left:5px}#mMenu{width:56px;border:1px solid #9b9b9b;position:absolute;right:7px;top:23px;display:none;background:#fff}#mMenu a{width:100%;height:100%;color:#00c;display:block;line-height:22px;text-indent:6px;text-decoration:none;filter:none\9}#mMenu a:hover{background:#ebebeb}#mMenu .ln{height:1px;background:#ebebeb;overflow:hidden;font-size:1px;line-height:1px;margin-top:-1px}


​    
    #index_guide{display:none}#index_logo{display:none}#u1{display:none}.s_ipt_wr{height:32px}body{padding:0}.s_form:after,.s_tab:after{content:".";display:block;height:0;clear:both;visibility:hidden}.s_form{zoom:1;height:63px;padding:0 0 0 10px}
    
    #result_logo{float:left;margin:11px 6px 0 6px}#result_logo img{width:104px}
    
    #head{padding:0;margin:0;width:100%;position:absolute;z-index:301;min-width:1000px;background:#fff;border-bottom:1px solid #ebebeb;position:fixed;_position:absolute}#head .head_wrapper{_width:1000px}#head.s_down{box-shadow:0 0 5px #888}.fm{clear:none;float:left;margin:15px 0 0 12px}#s_tab{background:#f8f8f8;line-height:36px;height:38px;padding:63px 0 0 138px;float:none;zoom:1}#s_tab a,#s_tab b{width:54px;display:inline-block;text-decoration:none;text-align:center;color:#666;font-size:14px}#s_tab b{border-bottom:2px solid #38f;font-weight:bold;color:#323232}#s_tab a:hover{color:#323232}#content_left{width:540px;padding-left:138px;padding-top:5px}#content_right{margin-top:45px}
    #page{padding:0 0 0 138px;margin:30px 0 40px 0}


​    
    #help{background:#f5f6f5;zoom:1;padding:0 0 0 50px;float:right}#help a{color:#777;padding:0 15px;text-decoration:none}#help a:hover{color:#333}
    
    #foot{background:#f5f6f5;border-top:1px solid #ebebeb;text-align:left;height:42px;line-height:42px}#foot .foot_c{float:left;padding:0 0 0 138px}.content_none{padding:30px 0 0 138px}
    
    #mCon{top:5px}
    
    .s_ipt_wr.bg,.s_btn_wr.bg,#su.bg{background-image:none}.s_btn_wr{width:auto;height:auto;border-bottom:1px solid transparent;*border-bottom:0}.s_btn{width:100px;height:34px;color:white;letter-spacing:1px;background:#3385ff;border-bottom:1px solid #2d78f4;outline:medium;*border-bottom:0;-webkit-appearance:none;-webkit-border-radius:0}.s_btn.btnhover{background:#317ef3;border-bottom:1px solid #2868c8;*border-bottom:0;box-shadow:1px 1px 1px #ccc}
    
    .s_btn_h{background:#3075dc;box-shadow:inset 1px 1px 3px #2964bb;-webkit-box-shadow:inset 1px 1px 3px #2964bb;-moz-box-shadow:inset 1px 1px 3px #2964bb;-o-box-shadow:inset 1px 1px 3px #2964bb}#head .bdsug{top:33px}.bdsug{width:538px;border-color:#ccc;box-shadow:1px 1px 3px #ededed;-webkit-box-shadow:1px 1px 3px #ededed;-moz-box-shadow:1px 1px 3px #ededed;-o-box-shadow:1px 1px 3px #ededed}
    
    .bdsug.bdsugbg{background-repeat:no-repeat;background-position:100% 100%;background-size:100px 110px;background-image:url(http://s1.bdstatic.com/r/www/cache/static/home/img/sugbg_6a9201c2.png);background-image:url(http://s1.bdstatic.com/r/www/cache/static/home/img/sugbg_d24a0811.gif)\9}.bdsug li{width:522px;line-height:22px}.bdsug li.bdsug-s{background:#f0f0f0}.bdsug-ala h3{margin:8px 0 5px 0}#wrapper_wrapper .container_l .EC_ppim_top,#wrapper_wrapper .container_xl .EC_ppim_top{width:640px}#wrapper_wrapper .container_s .EC_ppim_top{width:570px}#head .c-icon-bear-round{display:none}.container_l #content_right{width:384px}.container_l{width:1212px}.container_xl #content_right{width:384px}.container_xl{width:1257px}.index_tab_top{display:none}.index_tab_bottom{display:none}#lg{display:none}#m{display:none}#ftCon{display:none}#ent_sug{margin:40px 0 0 145px;font-size:13px;color:#666}.c-icon{background:url(http://s1.bdstatic.com/r/www/cache/static/global/img/icons_3bfb8e45.png) no-repeat 0 0;_background-image:url("http://s1.bdstatic.com/r/www/cache/static/global/img/icons_f72fb1cc.gif")}


​    
​    
    </style>
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <title>é¡µé¢ä¸å­å¨_ç¾åº¦æç´¢</title>
    
    <style data-for="debug">
    	#debug{display:none!important}
    </style>
    
    <style data-for="result" id="css_index_result">
    #seth{display:none;behavior:url(#default#homepage)}#setf{display:none}#sekj{margin-left:14px}#st,#sekj{display:none}.s_ipt_wr{border:1px solid #b6b6b6;border-color:#7b7b7b #b6b6b6 #b6b6b6 #7b7b7b;background:#fff;display:inline-block;vertical-align:top;width:539px;margin-right:0;border-right-width:0;border-color:#b8b8b8 transparent #ccc #b8b8b8}/*.wrapper_s .s_ipt_wr{width:439px}*//*.wrapper_s .s_ipt{width:434px}*/.s_ipt_wr:hover,.s_ipt_wr.ipthover{border-color:#999 transparent #b3b3b3 #999}.s_ipt_wr.iptfocus{border-color:#4791ff transparent #4791ff #4791ff}.s_ipt_tip{color:#aaa;position:absolute}.s_ipt{width:526px;height:22px;font:16px/22px arial;margin:6px 0 0 7px;padding:0;background:transparent;border:0;outline:0;-webkit-appearance:none}#kw{position:relative}.bdpfmenu,.usermenu{border:1px solid #d1d1d1;position:absolute;width:105px;top:36px;padding:1px 0;z-index:302;overflow:hidden;box-shadow:1px 1px 5px #d1d1d1;-webkit-box-shadow:1px 1px 5px #d1d1d1;-moz-box-shadow:1px 1px 5px #d1d1d1;-o-box-shadow:1px 1px 5px #d1d1d1}
    .bdpfmenu{font-size:12px}.bdpfmenu a,.usermenu a{display:block;text-align:left;margin:0!important;padding:0 9px;line-height:26px;text-decoration:none}
    
    #u .bri:hover,#u .bri.brihover{background-position:-18px 3px}#mCon #imeSIcon{background-position:-408px -144px;margin-left:0}#mCon span{color:#333}.bdpfmenu a:link,.bdpfmenu a:visited,#u .usermenu a:link,#u .usermenu a:visited{background:white;color:#333}.bdpfmenu a:hover,.bdpfmenu a:active,#u .usermenu a:hover,#u .usermenu a:active{background:#38f;text-decoration:none;color:white}.bdpfmenu{width:70px}.usermenu{width:68px;right:8px}#wrapper .bdnuarrow{width:24px;height:13px;position:absolute;z-index:303;top:24px;background:url(http://s1.bdstatic.com/r/www/cache/static/home/img/sugbg_6a9201c2.png) no-repeat -90px -1px;background-size:300px 21px;background-image:url(http://s1.bdstatic.com/r/www/cache/static/home/img/icons_0a1fc6ac.gif)\9}#prefpanel{background:#fafafa;display:none;opacity:0;position:fixed;_position:absolute;top:-359px;z-index:500;width:100%;min-width:960px;height:359px;border-bottom:1px solid #ebebeb}#prefpanel form{_width:850px}#kw_tip{cursor:default;display:none}#bds-message-wrapper{top:43px}
    
    input::-ms-clear{display:none}
    </style>
    
    </head>
    
    <body link="#0000cc">
    <div id="wrapper" style="" class="wrapper_s">
    
     <div id="head"> <div class="head_wrapper"> <div class="s_form"> <div class="s_form_wrapper"> <div id="lg"> <img hidefocus="true" src="//www.baidu.com/img/bd_logo1.png" width="270" height="129"> </div> <a href="/" id="result_logo" onmousedown="return c({'fm':'tab','tab':'logo'})"> <img src="//www.baidu.com/img/baidu_jgylogo3.gif" alt="å°ç¾åº¦é¦é¡µ" title="å°ç¾åº¦é¦é¡µ"> </a> <form id="form" name="f" action="/s" class="fm"> <input type="hidden" name="ie" value="utf-8"> <input type="hidden" name="f" value="8"> <input type="hidden" name="rsv_bp" value="1"> <input type="hidden" name="rsv_idx" value="1"> <input type="hidden" name="ch" value=""> <input type="hidden" name="tn" value="baiduerr"> <input type="hidden" name="bar" value=""> <span class="bg s_ipt_wr"> <input id="kw_tip" unselectable="on" onselectstart="return false;" class="s_ipt s_ipt_tip" disabled="" autocomplete="off" value="" maxlength="100" style="display: none;"> <input id="kw" name="wd" class="s_ipt" value="" maxlength="100" autocomplete="off"> </span><span class="bg s_btn_wr"> <input type="submit" id="su" value="ç¾åº¦ä¸ä¸" class="bg s_btn"> </span><span class="tools"> <span id="mHolder"> <div id="mCon"> <span>è¾å¥æ³</span> </div> <ul id="mMenu"> <li><a href="javascript:;" name="ime_hw">æå</a> </li> <li><a href="javascript:;" name="ime_py">æ¼é³</a> </li> <li class="ln"></li> <li><a href="javascript:;" name="ime_cl">å³é­</a> </li> </ul> </span> <span class="shouji" style="display: none;"><a href="http://w.x.baidu.com/go/mini/8/10000020" onmousedown="return ns_c({'fm':'behs','tab':'bdbrowser'})">ç¾åº¦æµè§å¨ï¼æå¼ç½é¡µå¿«2ç§ï¼</a> </span> </span> <input type="hidden" name="rn" value=""> <input type="hidden" name="rsv_enter" value="1"> </form> <div id="m"></div> </div></div> </div></div> <div class="s_tab" id="s_tab"> <b>ç½é¡µ</b> <a href="http://news.baidu.com/ns?cl=2&amp;rn=20&amp;tn=news&amp;word=" wdfield="word" onmousedown="return c({'fm':'tab','tab':'news'})">æ°é»</a><a href="http://tieba.baidu.com/f?kw=&amp;fr=wwwt" wdfield="kw" onmousedown="return c({'fm':'tab','tab':'tieba'})">è´´å§</a><a href="http://zhidao.baidu.com/q?ct=17&amp;pn=0&amp;tn=ikaslist&amp;rn=10&amp;word=&amp;fr=wwwt" wdfield="word" onmousedown="return c({'fm':'tab','tab':'zhidao'})">ç¥é</a><a href="http://music.baidu.com/search?fr=ps&amp;key=" wdfield="key" onmousedown="return c({'fm':'tab','tab':'music'})">é³ä¹</a><a href="http://image.baidu.com/i?tn=baiduimage&amp;ps=1&amp;ct=201326592&amp;lm=-1&amp;cl=2&amp;nc=1&amp;word=" wdfield="word" onmousedown="return c({'fm':'tab','tab':'pic'})">å¾ç</a><a href="http://v.baidu.com/v?ct=301989888&amp;rn=20&amp;pn=0&amp;db=0&amp;s=25&amp;word=" wdfield="word" onmousedown="return c({'fm':'tab','tab':'video'})">è§é¢</a><a href="http://map.baidu.com/m?word=&amp;fr=ps01000" wdfield="word" onmousedown="return c({'fm':'tab','tab':'map'})">å°å¾</a><a href="http://wenku.baidu.com/search?word=&amp;lm=0&amp;od=0" wdfield="word" onmousedown="return c({'fm':'tab','tab':'wenku'})">æåº</a><a href="//www.baidu.com/more/" onmousedown="return c({'fm':'tab','tab':'more'})">æ´å¤Â»</a> </div>
    <div id="ftCon"><div id="ftConw"><p id="lh"> <a id="seth" onclick="h(this)" href="/" onmousedown="return ns_c({'fm':'behs','tab':'homepage','pos':0})">æç¾åº¦è®¾ä¸ºä¸»é¡µ</a><a id="setf" href="http://www.baidu.com/cache/sethelp/index.html" onmousedown="return ns_c({'fm':'behs','tab':'favorites','pos':0})" target="_blank" style="display: inline;">æç¾åº¦è®¾ä¸ºä¸»é¡µ</a><a onmousedown="return ns_c({'fm':'behs','tab':'tj_about'})" href="http://home.baidu.com">å³äºç¾åº¦</a><a onmousedown="return ns_c({'fm':'behs','tab':'tj_about_en'})" href="http://ir.baidu.com">About Baidu</a> </p> <p id="cp">Â©2014&nbsp;Baidu&nbsp;<a href="/duty/" name="tj_duty">ä½¿ç¨ç¾åº¦åå¿è¯»</a>&nbsp;äº¬ICPè¯030173å·&nbsp;<i class="c-icon-icrlogo"></i> </p> </div> </div>
    <div id="wrapper_wrapper" style="display: block;">
    	<style>
    			.nors{
    				position: relative;
    			}
    			.norsTitle{
    				font-size: 22px;
    				font-family: Microsoft Yahei;
    				font-weight: normal;
    				color: #333;
    				margin: 35px 0 25px 0;
    			}
    			.norsSuggest {
    				display: inline-block;
    				color:#333;
    				font-family:arial;
    				font-size: 13px;
    				position: relative;
    			}
    
    			.norsSuggest li{
    				list-style: decimal;
    			}
    			.norsTitle2 {
    				font-family: arial;
    				font-size: 13px;
    				color: #666;	
    			}
    			.norsSuggest li{
    				margin: 13px 0;
    			}
    			.norsSuggest ol{
    				margin-left: 47px;
    			}
    			#foot{
    				position: fixed;
    				_position: absolute;
    				bottom: 0;
    				width: 100%;
    				clear: both;
    			}
    	</style>
    	<div id="content_left">
    		<div class="nors">
    			<div class="norsSuggest">
    				<h3 class="norsTitle">å¾æ±æ­ï¼æ¨è¦è®¿é®çé¡µé¢ä¸å­å¨ï¼</h3>
    				<p class="norsTitle2">æ¸©é¦¨æç¤ºï¼</p>
    				<ol>
    					<li>è¯·æ£æ¥æ¨è®¿é®çç½åæ¯å¦æ­£ç¡®</li> 
    					<li>å¦ææ¨ä¸è½ç¡®è®¤è®¿é®çç½åï¼è¯·æµè§<a href="http://www.baidu.com/more/index.html">ç¾åº¦æ´å¤</a>é¡µé¢æ¥çæ´å¤ç½åã</li>
    					<li>åå°é¡¶é¨éæ°åèµ·æç´¢</li>
    					<li>å¦æä»»ä½æè§æå»ºè®®ï¼è¯·åæ¶<a href="http://qingting.baidu.com/index">åé¦ç»æä»¬</a>ã</li>


​    
    				</ol>
    			</div>
    		</div>
    	</div>
    
    <div id="foot"><span class="foot_c">Â©2015&nbsp;Baidu&nbsp;<span>æ­¤åå®¹ç³»ç¾åº¦æ ¹æ®æ¨çæä»¤èªå¨æç´¢çç»æï¼ä¸ä»£è¡¨ç¾åº¦èµæè¢«æç´¢ç½ç«çåå®¹æç«åº</span></span>
    <span id="help"><a href="http://www.baidu.com/search/jubao.html" target="_blank">ä¸¾æ¥</a></span></div>
    
    <div class="c-tips-container" id="c-tips-container"></div></div></div><div class="c-tips-container" id="c-tips-container"></div>
    
    </body></html>


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
    During handling of the above exception, another exception occurred:


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


    JSONDecodeError: Expecting value: line 1 column 1 (char 0)


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
