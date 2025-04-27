async function startDetection() {
  const url = document.getElementById('urlInput').value;
  if (!url) {
      alert('请输入有效的URL');
      return;
  }

  // 更新状态
  document.getElementById('vulnerabilityResult').innerHTML = '<div class="loading">检测中...</div>';
  document.getElementById('testingMethodResult').innerHTML = '<div class="loading">检测中...</div>';

  try {
      // 调用后端API
      const response = await fetch('/api/detect', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: url })
      });

      const data = await response.json();

      // 更新结果
      document.getElementById('vulnerabilityResult').innerHTML = 
          (data.vul || '未检测到明显漏洞').replace(/\n/g, '<br>');
      document.getElementById('testingMethodResult').innerHTML = 
          (data.method || '无需特别测试方法').replace(/\n/g, '<br>');
  } catch (error) {
      console.error('检测失败:', error);
      document.getElementById('vulnerabilityResult').innerHTML = '检测失败，请重试';
      document.getElementById('testingMethodResult').innerHTML = '服务不可用';
  }
}