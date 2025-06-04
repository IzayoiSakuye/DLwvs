<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>XSS 演示</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    .output { margin-top: 10px; background: #f7f9fa; padding: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h2>反射型 XSS 演示页面</h2>
  <form method="get" action="xss_vulnerable.html">
    <label>请输入你的名字：<input type="text" name="name" /></label>
    <input type="submit" value="提交" />
  </form>

  <div class="output">
    <?php
      // 注意：此文件扩展名为 .html，为了让 PHP 生效，需要在服务器配置将 .html 解析为 PHP 文件，或将后缀改为 .php
      if (isset($_GET['name'])) {
        // 没有做任何转义，直接 echo
        echo "欢迎，" . $_GET['name'];
      } else {
        echo "欢迎，请输入你的名字。";
      }
    ?>
  </div>

  <hr>
  <p><strong>示例：</strong>在 URL 中输入 <code>?name=&lt;script&gt;alert('XSS')&lt;/script&gt;</code>，点击提交后会弹出脚本，说明存在 XSS 漏洞。</p>
</body>
</html>
