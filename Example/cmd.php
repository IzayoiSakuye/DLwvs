<?php
// command_injection.php
// 演示命令注入漏洞：直接把用户输入拼到 shell 命令里

$result_output = "";
$error_msg = "";

if (isset($_GET['host'])) {
    $host = $_GET['host'];
    // 直接拼接到 system() 中，没有过滤
    // 例如输入 127.0.0.1; ls 会先 ping 再执行 ls
    $cmd = "ping -c 2 " . $host;
    // 为了防止页面卡死，下面加 @ 和 2>&1 来捕获错误
    ob_start();
    @system($cmd . " 2>&1");
    $result_output = ob_get_clean();
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>命令注入 演示</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    input { padding: 5px; }
    .output { margin-top: 10px; background: #f7f9fa; padding: 10px; border: 1px solid #ccc; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h2>命令注入 演示页面</h2>
  <form method="get" action="command_injection.php">
    <label>输入 IP 或 域名：<input type="text" name="host" /></label>
    <input type="submit" value="Ping" />
  </form>

  <?php if (isset($_GET['host'])): ?>
    <div class="output">
      <strong>执行命令：</strong><code><?php echo "ping -c 2 " . htmlspecialchars($host); ?></code>
      <hr>
      <pre><?php echo htmlspecialchars($result_output ?: "无输出"); ?></pre>
    </div>
  <?php endif; ?>

  <hr>
  <p><strong>示例：</strong>在输入框中填入 <code>127.0.0.1; ls</code>，会先 ping 本地，再执行 <code>ls</code> 列出当前目录文件。</p>
</body>
</html>
