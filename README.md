# DLwvs

基于深度学习的 Web 漏洞扫描器

## 功能

- 支持常见 Web 漏洞检测：SQL 注入、XSS、命令执行等
- 使用深度学习模型进行智能漏洞识别，提高命中率并减少误报
- 提供 Web 界面和命令行两种使用方式，灵活方便

## 环境要求

- Python 3.7+
- Flask
- scikit-learn
- requests

## 安装与运行

1. 克隆仓库并进入目录：

   ```bash
   git clone https://github.com/IzayoiSakuye/DLwvs.git
   cd DLwvs
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动应用：

   ```bash
   python app.py
   ```

4. 浏览器打开并访问：[http://127.0.0.1:5000](http://127.0.0.1:5000/)



## 项目结构

```
DLwvs/
├── app.py                # 应用入口，包含 Flask 服务和命令行扫描逻辑
├── web/                  # 前端模板与静态资源
│   ├── templates/        # HTML 模板文件
│   └── static/           # CSS、JavaScript 等静态资源
└── README.md             # 项目说明文档
```

