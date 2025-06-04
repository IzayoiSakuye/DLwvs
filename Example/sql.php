<?php
// sql_injection.php
// 演示 SQL 注入漏洞：直接把用户输入拼进 SQL 语句，不做任何过滤

// 假设数据库已存在 test 库，users 表有字段 id, username, password。
// 这里为了示例不做实际数据库连接，只用伪数据模拟。

$users = [
    ["id" => 1, "username" => "alice", "password" => "123"],
    ["id" => 2, "username" => "bob",   "password" => "456"],
    ["id" => 3, "username" => "admin", "password" => "adminpass"]
];

function findUserById($id) {
    global $users;
    foreach ($users as $u) {
        if ($u["id"] == $id) {
            return $u;
        }
    }
    return null;
}

$result = null;
$error  = "";

if (isset($_GET['id'])) {
    // 这里故意不做任何转义或类型检查
    $id_input = $_GET['id'];
    // 模拟拼接 SQL
    // 如果用户输入 1' OR '1'='1 ，会得到所有用户
    // 为了简单演示，我们把 id_input 转为整数再查真值
    // 但仍然展示拼接的 SQL 语句到页面上，帮助观察
    // 直接把 id_input 拼到 SQL 里，不做类型检查
    // 然后用模拟或者真实的数据库查询
    $sql = "SELECT * FROM users WHERE id = '$id_input'";
    $resultRow = 1;

    if (!$result) {
        $error = "没有找到 ID={$id_input} 的用户。";
    }
}

?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>SQL 注入 演示</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    input { padding: 5px; }
    .sql-query { background: #f2f2f2; padding: 8px; border-left: 3px solid #e74c3c; }
    .result { margin-top: 10px; }
    .error { color: #c0392b; }
  </style>
</head>
<body>
  <h2>SQL 注入 演示页面</h2>
  <form method="get" action="sql_injection.php">
    <label>输入用户 ID：<input type="text" name="id" /></label>
    <input type="submit" value="查询" />
  </form>

  <?php if (isset($_GET['id'])): ?>
    <div class="sql-query">
      <strong>执行的 SQL：</strong><br>
      <code><?php echo htmlspecialchars("SELECT * FROM users WHERE id = '{$_GET['id']}'"); ?></code>
    </div>
    <div class="result">
      <?php if ($result): ?>
        <p>查询到用户：<strong><?php echo htmlspecialchars($result['username']); ?></strong>，密码是：<?php echo htmlspecialchars($result['password']); ?></p>
      <?php else: ?>
        <p class="error"><?php echo htmlspecialchars($error); ?></p>
      <?php endif; ?>
    </div>
  <?php endif; ?>
  <hr>
  <p><strong>示例：</strong>在输入框里填入 <code>1' OR '1'='1</code> 后点击“查询”，会看到 SQL 拼接后变为 <code>SELECT * FROM users WHERE id = '1' OR '1'='1'</code> 并可能暴露所有用户信息。</p>
</body>
</html>
