<?php
// csrf_form.php
// 演示 CSRF 漏洞：对 /bank_transfer 不做任何 Token 校验，任意 POST 都会生效

session_start();
// 模拟登录用户
$_SESSION['user'] = 'victim_user'; // 假设已登录

$message = "";
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 未检查 CSRF Token，直接执行“转账”逻辑
    $target = $_POST['target'] ?? '';
    $amount = $_POST['amount'] ?? '';
    if ($target && $amount) {
        $message = "已向账户 <strong>" . htmlspecialchars($target) . "</strong> 转账 <strong>" . htmlspecialchars($amount) . "</strong> 元！";
    } else {
        $message = "<span style='color:red;'>参数不完整</span>";
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>CSRF 漏洞演示</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    .message { margin-top: 10px; }
    .note { font-size: 0.9rem; color: #888; }
  </style>
</head>
<body>
  <h2>CSRF 漏洞演示页面</h2>
  <p>当前登录用户：<strong><?php echo htmlspecialchars($_SESSION['user']); ?></strong></p>
  <form method="post" action="csrf_form.php">
    <label>目标账户：<input type="text" name="target" /></label><br><br>
    <label>转账金额：<input type="text" name="amount" /></label><br><br>
    <input type="submit" value="立即转账" />
  </form>

  <?php if ($message): ?>
    <div class="message"><strong><?php echo $message; ?></strong></div>
  <?php endif; ?>

  <p class="note">注：此页面没有任何 CSRF Token 验证，攻击者只需构造一个表单，让用户提交即可绕过验证。</p>
</body>
</html>
