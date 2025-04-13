import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse, parse_qs
import re
import logging
from tqdm import tqdm

class HTTPDataProcessor:
    def __init__(self, input_dir: str, output_dir: str):
        """
        初始化HTTP数据处理器
        
        Args:
            input_dir: 输入数据目录
            output_dir: 输出数据目录
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.setup_logging()
        self.setup_directories()
        
        # 定义漏洞类型
        self.vulnerability_types = {
            'sql_injection': ['sql injection', 'sqli', 'sql注入'],
            'xss': ['cross-site scripting', 'xss', '跨站脚本'],
            'csrf': ['cross-site request forgery', 'csrf', '跨站请求伪造'],
            'rce': ['remote code execution', 'rce', '远程代码执行'],
            'file_inclusion': ['file inclusion', 'lfi', 'rfi', '文件包含'],
            'path_traversal': ['path traversal', 'directory traversal', '路径遍历'],
            'command_injection': ['command injection', 'cmd injection', '命令注入'],
            'ssrf': ['server-side request forgery', 'ssrf', '服务器端请求伪造'],
            'xxe': ['xml external entity', 'xxe', 'xml外部实体'],
            'deserialization': ['deserialization', 'unsafe deserialization', '反序列化'],
            'other': ['other', '其他']
        }

        # 定义安全（无漏洞）的关键词
        self.secure_keywords = [
            'secure', 'safe', 'normal', 'clean',
            '安全', '正常', '无漏洞', '已修复'
        ]
        
        # 定义要提取的特征
        self.request_features = [
            'method',
            'url',
            'path',
            'query_params',
            'headers',
            'body',
            'content_type',
            'content_length'
        ]
        
        self.response_features = [
            'status_code',
            'headers',
            'body',
            'content_type',
            'content_length'
        ]

    def setup_logging(self):
        """设置日志配置"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('http_data_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_directories(self):
        """创建必要的目录"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'train'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'val'), exist_ok=True)

    def parse_request(self, request_data: Dict) -> Dict:
        """
        解析HTTP请求数据
        
        Args:
            request_data: 原始请求数据字典
            
        Returns:
            解析后的请求特征字典
        """
        try:
            parsed = {}
            
            # 提取基本信息
            parsed['method'] = request_data.get('method', '')
            parsed['url'] = request_data.get('url', '')
            
            # 解析URL
            url_parts = urlparse(parsed['url'])
            parsed['path'] = url_parts.path
            parsed['query_params'] = dict(parse_qs(url_parts.query))
            
            # 处理headers
            headers = request_data.get('headers', {})
            parsed['headers'] = headers
            parsed['content_type'] = headers.get('Content-Type', '')
            parsed['content_length'] = headers.get('Content-Length', 0)
            
            # 处理body
            parsed['body'] = request_data.get('body', '')
            
            return parsed
            
        except Exception as e:
            self.logger.error(f"解析请求数据时出错: {str(e)}")
            return {}

    def parse_response(self, response_data: Dict) -> Dict:
        """
        解析HTTP响应数据
        
        Args:
            response_data: 原始响应数据字典
            
        Returns:
            解析后的响应特征字典
        """
        try:
            parsed = {}
            
            # 提取基本信息
            parsed['status_code'] = response_data.get('status_code', 0)
            
            # 处理headers
            headers = response_data.get('headers', {})
            parsed['headers'] = headers
            parsed['content_type'] = headers.get('Content-Type', '')
            parsed['content_length'] = headers.get('Content-Length', 0)
            
            # 处理body
            parsed['body'] = response_data.get('body', '')
            
            return parsed
            
        except Exception as e:
            self.logger.error(f"解析响应数据时出错: {str(e)}")
            return {}

    def extract_features(self, data: Dict) -> Tuple[Dict, Dict]:
        """
        从原始数据中提取特征
        
        Args:
            data: 包含请求和响应的原始数据
            
        Returns:
            请求特征和响应特征的元组
        """
        request_features = self.parse_request(data.get('request', {}))
        response_features = self.parse_response(data.get('response', {}))
        return request_features, response_features

    def normalize_features(self, features: Dict) -> Dict:
        """
        标准化特征值
        
        Args:
            features: 原始特征字典
            
        Returns:
            标准化后的特征字典
        """
        normalized = {}
        
        for key, value in features.items():
            if isinstance(value, (str, bytes)):
                # 将字符串转换为小写并移除多余空白
                normalized[key] = str(value).lower().strip()
            elif isinstance(value, (int, float)):
                # 数值标准化到0-1范围
                normalized[key] = float(value) / (1 + float(value))  # 避免除以0
            elif isinstance(value, dict):
                # 递归处理嵌套字典
                normalized[key] = self.normalize_features(value)
            elif isinstance(value, (list, tuple)):
                # 处理列表
                normalized[key] = [str(item).lower().strip() if isinstance(item, (str, bytes))
                                 else item for item in value]
            else:
                normalized[key] = value
                
        return normalized

    def identify_vulnerability_type(self, data: Dict) -> Tuple[Set[str], bool]:
        """
        识别漏洞类型和安全状态
        
        Args:
            data: 原始数据字典
            
        Returns:
            漏洞类型集合和是否安全的元组
        """
        vuln_types = set()
        
        # 获取所有可能包含漏洞信息的字段
        text_to_check = [
            str(data.get('vulnerability_description', '')),
            str(data.get('title', '')),
            str(data.get('description', '')),
            str(data.get('security_status', '')),  # 新增安全状态字段
            str(data.get('request', {}).get('body', '')),
            str(data.get('response', {}).get('body', '')),
        ]
        text_to_check = ' '.join(text_to_check).lower()
        
        # 首先检查是否明确标记为安全
        is_secure = False
        for keyword in self.secure_keywords:
            if keyword.lower() in text_to_check:
                is_secure = True
                break
        
        # 如果没有明确标记为安全，则检查漏洞类型
        if not is_secure:
            for vuln_type, keywords in self.vulnerability_types.items():
                for keyword in keywords:
                    if keyword.lower() in text_to_check:
                        vuln_types.add(vuln_type)
                        break
        
        return vuln_types, is_secure

    def create_vulnerability_labels(self, vuln_types: Set[str]) -> Dict[str, int]:
        """
        创建漏洞标签字典
        
        Args:
            vuln_types: 漏洞类型集合
            
        Returns:
            漏洞标签字典
        """
        labels = {vuln_type: 0 for vuln_type in self.vulnerability_types.keys()}
        for vuln_type in vuln_types:
            labels[vuln_type] = 1
        return labels

    def process_file(self, file_path: str) -> List[Dict]:
        """
        处理单个数据文件
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            处理后的数据列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            processed_data = []
            
            # 如果数据是列表，处理每个项
            if isinstance(data, list):
                for item in data:
                    request_features, response_features = self.extract_features(item)
                    
                    # 识别漏洞类型和安全状态
                    vuln_types, is_secure = self.identify_vulnerability_type(item)
                    vuln_labels = self.create_vulnerability_labels(vuln_types)
                    
                    processed_item = {
                        'request': self.normalize_features(request_features),
                        'response': self.normalize_features(response_features),
                        'vulnerability_types': list(vuln_types),
                        'labels': vuln_labels,
                        'is_vulnerable': 1 if vuln_types else 0,
                        'is_secure': 1 if is_secure else 0,
                        'security_status': 'secure' if is_secure else ('vulnerable' if vuln_types else 'unknown')
                    }
                    processed_data.append(processed_item)
            else:
                # 单个数据项
                request_features, response_features = self.extract_features(data)
                
                # 识别漏洞类型和安全状态
                vuln_types, is_secure = self.identify_vulnerability_type(data)
                vuln_labels = self.create_vulnerability_labels(vuln_types)
                
                processed_item = {
                    'request': self.normalize_features(request_features),
                    'response': self.normalize_features(response_features),
                    'vulnerability_types': list(vuln_types),
                    'labels': vuln_labels,
                    'is_vulnerable': 1 if vuln_types else 0,
                    'is_secure': 1 if is_secure else 0,
                    'security_status': 'secure' if is_secure else ('vulnerable' if vuln_types else 'unknown')
                }
                processed_data.append(processed_item)
                
            return processed_data
            
        except Exception as e:
            self.logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            return []

    def split_dataset(self, data: List[Dict], train_ratio=0.7, val_ratio=0.15, test_ratio=0.15) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        将数据集分割为训练集、验证集和测试集
        
        Args:
            data: 完整数据集
            train_ratio: 训练集比例
            val_ratio: 验证集比例
            test_ratio: 测试集比例
            
        Returns:
            训练集、验证集和测试集的元组
        """
        # 首先分割出测试集
        train_val, test = train_test_split(data, test_size=test_ratio, random_state=42)
        
        # 然后从剩余数据中分割出验证集
        val_ratio_adjusted = val_ratio / (train_ratio + val_ratio)
        train, val = train_test_split(train_val, test_size=val_ratio_adjusted, random_state=42)
        
        return train, val, test

    def save_dataset(self, dataset: List[Dict], name: str):
        """
        保存数据集到文件
        
        Args:
            dataset: 要保存的数据集
            name: 数据集名称（train/val/test）
        """
        output_path = os.path.join(self.output_dir, name)
        
        # 保存为JSON格式
        with open(f"{output_path}/data.json", 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
            
        # 转换为DataFrame并保存为CSV格式
        df = pd.json_normalize(dataset)
        df.to_csv(f"{output_path}/data.csv", index=False)
        
        self.logger.info(f"已保存{name}数据集，包含 {len(dataset)} 条记录")

    def process_all_data(self):
        """处理所有数据文件并生成数据集"""
        all_data = []
        vulnerability_stats = {vuln_type: 0 for vuln_type in self.vulnerability_types.keys()}
        security_stats = {
            'secure': 0,
            'vulnerable': 0,
            'unknown': 0
        }
        
        # 获取所有JSON文件
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]
        
        if not json_files:
            self.logger.warning(f"在目录 {self.input_dir} 中未找到JSON文件")
            return
            
        self.logger.info(f"开始处理 {len(json_files)} 个数据文件")
        
        # 处理每个文件
        for json_file in tqdm(json_files, desc="处理数据文件"):
            file_path = os.path.join(self.input_dir, json_file)
            processed_data = self.process_file(file_path)
            
            # 更新统计信息
            for item in processed_data:
                security_stats[item['security_status']] += 1
                if item['is_vulnerable']:
                    for vuln_type in item['vulnerability_types']:
                        vulnerability_stats[vuln_type] += 1
            
            all_data.extend(processed_data)
            
        # 分割数据集
        train_data, val_data, test_data = self.split_dataset(all_data)
        
        # 保存数据集
        self.save_dataset(train_data, 'train')
        self.save_dataset(val_data, 'val')
        self.save_dataset(test_data, 'test')
        
        # 输出统计信息
        self.logger.info("\n数据集处理完成:")
        self.logger.info(f"总数据量: {len(all_data)}")
        self.logger.info("\n安全状态统计:")
        self.logger.info(f"安全样本数: {security_stats['secure']}")
        self.logger.info(f"包含漏洞样本数: {security_stats['vulnerable']}")
        self.logger.info(f"未知状态样本数: {security_stats['unknown']}")
        self.logger.info("\n漏洞类型统计:")
        for vuln_type, count in vulnerability_stats.items():
            if count > 0:
                self.logger.info(f"{vuln_type}: {count} 条")
        self.logger.info(f"\n训练集: {len(train_data)} 条")
        self.logger.info(f"验证集: {len(val_data)} 条")
        self.logger.info(f"测试集: {len(test_data)} 条")

def main():
    # 设置输入输出目录
    input_dir = "RawData"  # 原始HTTP数据目录
    output_dir = "processed_data"  # 处理后的数据保存目录
    
    # 创建处理器实例并处理数据
    processor = HTTPDataProcessor(input_dir, output_dir)
    processor.process_all_data()

if __name__ == "__main__":
    main() 