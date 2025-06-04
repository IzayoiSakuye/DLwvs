<?php
// index.php
session_start();

// —— 1. 模拟“数据库”中的用户数据（仅演示，无需真实数据库） —— //
$users = [
    ["id" => 1, "username" => "alice", "password" => "123"],
    ["id" => 2, "username" => "bob",   "password" => "456"],
    ["id" => 3, "username" => "admin", "password" => "adminpass"]
];
function findUserById($id) {
    global $users;
    foreach ($users as $u) {
        if ($u["id"] == $id) return $u;
    }
    return null;
}

// —— 2. 模拟已登录用户，供 CSRF 漏洞演示用 —— //
if (!isset($_SESSION['user'])) {
    $_SESSION['user'] = 'victim_user'; // 假设登录用户
}

// —— 处理各类“提交” —— //
$sqlResult       = null;
$sqlError        = "";
$xssOutput       = "";
$cmdOutput       = "";
$uploadMessage   = "";
$csrfMessage     = "";

// ——— SQL 注入 演示 ——— //
if (isset($_GET['id'])) {
    $id_input = $_GET['id'];
    // 这里演示“直接把 id_input 拼到 SQL”而不做任何过滤
    $sql = "SELECT * FROM users WHERE id = '$id_input'";
    // 直接用 intval 查真值，以演示拼接SQL时的危险性
    $user = findUserById(intval($id_input));
    if ($user) {
        $sqlResult = $user;
    } else {
        $sqlError = "没有找到 ID=" . htmlspecialchars($id_input) . " 的用户。";
    }
}

// ——— XSS 演示 ——— //
if (isset($_GET['name'])) {
    // 直接把用户输入原样输出到页面，未做任何转义
    $xssOutput = $_GET['name'];
}

// ——— 命令注入 演示 ——— //
if (isset($_GET['hostname'])) {
    $host = $_GET['hostname'];
    // 直接拼到 system() 中，无任何过滤
    // Linux 下用 ping -c 1，如果是 Windows 可改为 ping -n 1
    $cmd = "ping -c 1 " . $host . " 2>&1";
    ob_start();
    @system($cmd);
    $cmdOutput = ob_get_clean();
}

// ——— 文件上传 演示 ——— //
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $uploadDir = __DIR__ . '/uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }
    $filename = basename($_FILES['file']['name']);
    $target   = $uploadDir . $filename;
    if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
        $uploadMessage = "文件上传成功，路径：<code>uploads/" . htmlspecialchars($filename) . "</code>";
    } else {
        $uploadMessage = "<span style='color:red;'>上传失败</span>";
    }
}

// ——— CSRF 演示 ——— //
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['csrf_target']) && isset($_POST['csrf_amount'])) {
    // 模拟未验证 CSRF Token，直接执行“转账”逻辑
    $target = $_POST['csrf_target'];
    $amount = $_POST['csrf_amount'];
    if ($target && $amount) {
        $csrfMessage = "已向账户 <strong>" . htmlspecialchars($target) . "</strong> 转账 <strong>" . htmlspecialchars($amount) . "</strong> 元！";
    } else {
        $csrfMessage = "<span style='color:red;'>参数不完整</span>";
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>靶场综合演示（五种漏洞）</title>
  <style>
    body { font-family: sans-serif; padding: 20px; background: #f2f5f8; }
    h2 { color: #2c3e50; margin-bottom: 15px; }
    .vul-section { background: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 15px; margin-bottom: 20px; }
    .vul-section h3 { margin-top: 0; color: #34495e; }
    input[type="text"], input[type="file"], button {
      padding: 6px 10px; margin-right: 10px; border: 1px solid #ccc; border-radius: 3px;
    }
    button { background: #1abc9c; color: #fff; border: none; cursor: pointer; }
    button:hover { background: #16a085; }
    .output { margin-top: 10px; background: #fafafa; padding: 10px; border: 1px solid #eee; white-space: pre-wrap; }
    .note { font-size: 0.9rem; color: #888; margin-top: 10px; }
    .snippet { background: #f7f9fa; padding: 8px; border: 1px solid #d1d5d9; border-radius: 3px; white-space: pre-wrap; }
    code { background: #f7f9fa; padding: 2px 4px; border-radius: 3px; }
  </style>
</head>
<body>
  <h2>靶场综合演示：SQL 注入、XSS、命令注入、文件上传、CSRF</h2>

  <!-- 1. SQL 注入 演示 -->
  <div class="vul-section">
    <h3>1. SQL 注入 演示</h3>
    <form method="get" action="">
      <label>输入用户 ID：<input type="text" name="id" /></label>
      <button type="submit">查询</button>
    </form>
    <?php if (isset($_GET['id'])): ?>
      <div class="output">
        <strong>执行的 SQL：</strong><br>
        <code><?php echo htmlspecialchars("SELECT * FROM users WHERE id = '{$_GET['id']}'"); ?></code>
        <hr>
        <?php if ($sqlResult): ?>
          查询到用户：<strong><?php echo htmlspecialchars($sqlResult['username']); ?></strong>，密码：<?php echo htmlspecialchars($sqlResult['password']); ?>
        <?php else: ?>
          <span style="color:red;"><?php echo htmlspecialchars($sqlError); ?></span>
        <?php endif; ?>
      </div>
    <?php endif; ?>
    <p class="note">示例：输入 <code>1' OR '1'='1</code> 再查询，可看到注入效果。</p>
  </div>

  <!-- 2. XSS 演示 -->
  <div class="vul-section">
    <h3>2. XSS 演示</h3>
    <form method="get" action="">
      <label>请输入你的名字：<input type="text" name="name" /></label>
      <button type="submit">提交</button>
    </form>
    <div class="output">
      <?php
        if ($xssOutput) {
          // 直接输出，不做 htmlspecialchars 转义，故意演示 XSS
          echo "欢迎，" . $xssOutput;
        } else {
          echo "欢迎，请输入你的名字。";
        }
      ?>
    </div>
    <p class="note">示例：输入 <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>，可触发弹窗。</p>
  </div>

  <!-- 3. 命令注入 演示 -->
  <div class="vul-section">
    <h3>3. 命令注入 演示</h3>
    <form method="get" action="">
      <label>输入 IP 或 主机名：<input type="text" name="hostname" /></label>
      <button type="submit">Ping</button>
    </form>
    <?php if (isset($_GET['hostname'])): ?>
      <div class="output">
        <strong>执行命令：</strong><code><?php echo "ping -c 1 " . htmlspecialchars($_GET['hostname']); ?></code>
        <hr>
        <div class="snippet"><?php echo htmlspecialchars($cmdOutput ?: "无输出"); ?></div>
      </div>
    <?php endif; ?>
    <p class="note">示例：输入 <code>127.0.0.1; ls</code>，可在输出里看到目录列表。</p>
  </div>

  <!-- 4. 文件上传 演示 -->
  <div class="vul-section">
    <h3>4. 文件上传 演示</h3>
    <form method="post" enctype="multipart/form-data" action="">
      <input type="file" name="file" />
      <button type="submit">上传</button>
    </form>
    <?php if ($uploadMessage): ?>
      <div class="output"><?php echo $uploadMessage; ?></div>
    <?php endif; ?>
    <p class="note">上传任意文件（包括 .php），成功后可通过访问 <code>http://localhost:8080/uploads/你上传的文件.php</code> 执行。</p>
  </div>

  <!-- 5. CSRF 演示 -->
  <div class="vul-section">
    <h3>5. CSRF 漏洞 演示</h3>
    <p>当前登录用户：<strong><?php echo htmlspecialchars($_SESSION['user']); ?></strong></p>
    <form method="post" action="">
      <label>目标账户：<input type="text" name="csrf_target" /></label><br><br>
      <label>转账金额：<input type="text" name="csrf_amount" /></label><br><br>
      <button type="submit">立即转账</button>
    </form>
    <?php if ($csrfMessage): ?>
      <div class="output"><strong><?php echo $csrfMessage; ?></strong></div>
    <?php endif; ?>
    <p class="note">此示例未检查 CSRF Token，任何页面嵌入此表单都可自动提交并转账。</p>
  </div>
</body>
</html>
