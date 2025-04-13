import os
import pandas as pd

# 加载数据
def load_samples(file_path, label, vuln_type):
    with open(file_path, 'r', encoding='utf-8') as f:
        samples = [line.strip() for line in f if line.strip()]
    return [{'text': sample, 'label': label, 'vuln_type': vuln_type} for sample in samples]

data = []

# SQL 样本
data += load_samples(r'e:\CS\repository\基于深度学习的漏洞扫描系统\DLwvs\data\train\bad_opcode_SQL.txt', 1, 'SQL')
data += load_samples(r'e:\CS\repository\基于深度学习的漏洞扫描系统\DLwvs\data\train\good_opcode_SQL.txt', 0, 'SQL')

# XSS 样本
data += load_samples(r'e:\CS\repository\基于深度学习的漏洞扫描系统\DLwvs\data\train\bad_opcode_XSS.txt', 1, 'XSS')
data += load_samples(r'e:\CS\repository\基于深度学习的漏洞扫描系统\DLwvs\data\train\good_opcode_XSS.txt', 0, 'XSS')

df = pd.DataFrame(data)
df.to_csv('train_dataset.csv', index=False, encoding='utf-8')
print("OK")