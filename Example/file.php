<?php
// file_upload.php
// 演示文件上传漏洞：不限制后缀、不检查类型，能直接把文件存到 uploads/ 目录

$message = "";
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        // 上传目录，需保证 web 服务器对 uploads/ 可写
        $uploadDir = __DIR__ . '/uploads/';
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0755, true);
        }
        $filename = basename($_FILES['file']['name']);
        $target = $uploadDir . $filename;
        if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
            $message = "文件上传成功，路径：<code>uploads/" . htmlspecialchars($filename) . "</code>";
        } else {
            $message = "<span style='color:red;'>上传失败</span>";
        }
    } else {
        $message = "<span style='color:red;'>未选择文件</span>";
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>文件上传 漏洞演示</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    .message { margin-top: 10px; }
    .note { font-size: 0.9rem; color: #888; }
  </style>
</head>
<body>
  <h2>文件上传 漏洞演示页面</h2>
  <form method="post" enctype="multipart/form-data" action="file_upload.php">
    <input type="file" name="file" />
    <input type="submit" value="上传" />
  </form>

  <?php if ($message): ?>
    <div class="message"><?php echo $message; ?></div>
  <?php endif; ?>

  <p class="note">注：此示例未限制可上传文件类型，用户可以上传任意后缀（包括 .php），然后通过访问 <code>http://localhost/uploads/你上传的文件.php</code> 执行代码。</p>
</body>
</html>
