// app.js
function isValidURL(str) {
  try {
    // 如果可以正常执行则是合法链接
    new URL(str);
    return true;
  } catch (e) {
    return false;
  }
}
async function startDetection() {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) {
    alert('请输入合法的URL');
    return;
  }
   // 增加“合法链接”校验
  if (!isValidURL(url)) {
    alert('请输入合法的URL');
    return;
  }

  
  // 显示“检测中”提示
  const vulnDiv = document.getElementById('vulnerabilityResult');
  const fixedDiv = document.getElementById('fixedSummary');
  const suggestionBox = document.getElementById('suggestionBox');
  vulnDiv.innerHTML = '<div class="loading">检测中...</div>';
  fixedDiv.innerHTML = '<div class="loading">检测中...</div>';
  suggestionBox.value = '检测中，请稍候...';

  try {
    const response = await fetch('/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await response.json();

    if (data.error) {
      vulnDiv.innerHTML = `<span class="error">错误：${data.error}</span>`;
      fixedDiv.innerHTML = '';
      suggestionBox.value = '';
      return;
    }

    const raw = data.raw_results;

    // 1. 构建 “可折叠” 漏洞详细信息
    let vulnHtml = '';
    for (const [vulType, info] of Object.entries(raw)) {
      // 生成 summary 文字：漏洞类型 + 检测结果（是/否）
      const resultText = info.vulnerable ? '存在可疑' : '未发现';
      const resultClass = info.vulnerable ? 'yes' : 'no';

      // 构造 <details> 结构
      vulnHtml += `<details>
        <summary>${vulType}：<span class="${resultClass}">${resultText}</span></summary>
        <div class="detail-content">
          <ul>`;

      // payload（GET 型）
      if (info.payload) {
        vulnHtml += `<li><strong>Payload：</strong><code>${info.payload}</code></li>`;
      }
      // upload_endpoint（文件上传型）
      if (info.upload_endpoint) {
        vulnHtml += `<li><strong>Upload Endpoint：</strong>${info.upload_endpoint}</li>`;
        vulnHtml += `<li><strong>File Name：</strong>${info.file_name}</li>`;
      }
      // CSRF POST 类型
      if (info.endpoint && info.params) {
        vulnHtml += `<li><strong>Endpoint：</strong>${info.endpoint}</li>`;
        vulnHtml += `<li><strong>Params：</strong>${JSON.stringify(info.params)}</li>`;
      }

      vulnHtml += `
            <li><strong>Status Code：</strong>${info.status_code === null ? '请求异常' : info.status_code}</li>
            <li><strong>响应片段：</strong><pre class="snippet">${info.snippet || ''}</pre></li>
          </ul>
        </div>
      </details>`;
    }
    vulnDiv.innerHTML = vulnHtml;

    // 2. 构建 “固定标题：检测结果” 区域
    let fixedHtml = '';
    for (const [vulType, info] of Object.entries(raw)) {
      const resultLabel = info.vulnerable ? '是' : '否';
      const resultClass = info.vulnerable ? 'yes' : 'no';
      fixedHtml += `<div class="item">
        <span class="label">${vulType}：</span>
        <span class="value ${resultClass}">${resultLabel}</span>
      </div>`;
    }
    fixedDiv.innerHTML = fixedHtml;

    // 3. 填充“修改建议”框，如果后端有 lm_summary，就显示；否则留空
    const suggestionDiv = document.getElementById('suggestionBox');
    let suggestionText = data.lm_summary && data.lm_summary !== '（模型调用失败或未启用）'
      ? data.lm_summary
      : '无修改建议。';

    // 使用 marked.js 把 Markdown 转为 HTML，然后插入到 suggestionDiv
    suggestionDiv.innerHTML = marked.parse(suggestionText);

  } catch (error) {
    console.error('检测失败:', error);
    vulnDiv.innerHTML = '<span class="error">检测失败，请重试</span>';
    fixedDiv.innerHTML = '<span class="error">综合结果不可用</span>';
    suggestionBox.value = '';
  }
}
