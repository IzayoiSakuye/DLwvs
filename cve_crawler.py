import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import random
from fake_useragent import UserAgent
import json
from datetime import datetime
import os
import concurrent.futures
from urllib.parse import quote

class CVEDetailsCrawler:
    def __init__(self):
        self.base_url = "https://www.cvedetails.com"
        self.ua = UserAgent()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        # 定义漏洞类型及其搜索关键词
        self.vulnerability_types = {
            'sql_injection': 'sql injection',
            'xss': 'cross site scripting',
            'csrf': 'cross site request forgery',
            'rce': 'remote code execution',
            'file_inclusion': 'file inclusion'
        }
        # 创建数据保存目录
        self.data_dir = "crawled_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_random_delay(self):
        """生成随机延迟时间，避免被反爬"""
        return random.uniform(1, 3)

    def _update_headers(self):
        """更新请求头，模拟不同的浏览器"""
        self.headers['User-Agent'] = self.ua.random

    def get_page(self, url):
        """获取页面内容"""
        max_retries = 3
        for retry in range(max_retries):
            try:
                self._update_headers()
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if retry == max_retries - 1:
                    print(f"获取页面失败: {url}")
                    print(f"错误信息: {str(e)}")
                    return None
                time.sleep(self._get_random_delay() * 2)
        return None

    def parse_vulnerability(self, cve_url):
        """解析单个漏洞详情页"""
        html = self.get_page(cve_url)
        if not html:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # 提取漏洞详情
            vuln_data = {
                'cve_id': soup.find('h1').text.strip(),
                'description': soup.find('div', {'class': 'cvedetailssummary'}).text.strip(),
                'cvss_score': soup.find('div', {'class': 'cvssbox'}).text.strip() if soup.find('div', {'class': 'cvssbox'}) else 'N/A',
                'vulnerability_type': [x.text.strip() for x in soup.find_all('span', {'class': 'vtype'})],
                'publish_date': soup.find('table', {'class': 'details'}).find('td', text='Publish Date').find_next_sibling('td').text.strip(),
                'update_date': soup.find('table', {'class': 'details'}).find('td', text='Update Date').find_next_sibling('td').text.strip(),
                'url': cve_url
            }
            
            # 提取漏洞评分详情
            score_table = soup.find('table', {'class': 'cvssbox'})
            if score_table:
                scores = {}
                for row in score_table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) == 2:
                        scores[cols[0].text.strip()] = cols[1].text.strip()
                vuln_data['cvss_details'] = scores

            # 提取受影响的产品信息
            affected_products = []
            products_table = soup.find('table', {'id': 'vulnprodstable'})
            if products_table:
                for row in products_table.find_all('tr')[1:]:  # 跳过表头
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        product_info = {
                            'vendor': cols[2].text.strip(),
                            'product': cols[3].text.strip(),
                            'version': cols[4].text.strip() if len(cols) > 4 else 'N/A'
                        }
                        affected_products.append(product_info)
            vuln_data['affected_products'] = affected_products

            return vuln_data
        except Exception as e:
            print(f"解析漏洞详情失败: {cve_url}")
            print(f"错误信息: {str(e)}")
            return None

    def crawl_vulnerabilities_by_type(self, vuln_type, start_page=1, end_page=10):
        """爬取指定类型的漏洞信息"""
        all_vulnerabilities = []
        search_keyword = self.vulnerability_types[vuln_type]
        
        for page in tqdm(range(start_page, end_page + 1), desc=f"爬取{vuln_type}漏洞进度"):
            # 构建搜索URL
            encoded_keyword = quote(search_keyword)
            search_url = f"{self.base_url}/vulnerability-list/vendor_id-0/product_id-0/version_id-0/keyword-{encoded_keyword}/page-{page}"
            
            html = self.get_page(search_url)
            if not html:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            vuln_table = soup.find('table', {'class': 'searchresults'})
            
            if not vuln_table:
                print(f"页面 {page} 未找到漏洞列表")
                continue

            # 获取所有漏洞链接
            vuln_links = vuln_table.find_all('a', href=True)
            vuln_urls = [f"{self.base_url}{link['href']}" for link in vuln_links if '/cve/' in link['href']]

            # 爬取每个漏洞的详细信息
            for url in vuln_urls:
                vuln_data = self.parse_vulnerability(url)
                if vuln_data:
                    vuln_data['crawled_type'] = vuln_type  # 添加爬取时的漏洞类型标记
                    all_vulnerabilities.append(vuln_data)
                time.sleep(self._get_random_delay())

            # 每爬取一页就保存一次数据
            self.save_data(all_vulnerabilities, f"{vuln_type}_vulnerabilities_page_{page}.json")
            
        return all_vulnerabilities

    def save_data(self, data, filename):
        """保存爬取的数据"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filepath}")

    def crawl_all_vulnerability_types(self, start_page=1, end_page=5):
        """爬取所有类型的漏洞"""
        all_results = {}
        
        for vuln_type in self.vulnerability_types.keys():
            print(f"\n开始爬取 {vuln_type} 类型的漏洞...")
            vulnerabilities = self.crawl_vulnerabilities_by_type(
                vuln_type=vuln_type,
                start_page=start_page,
                end_page=end_page
            )
            all_results[vuln_type] = vulnerabilities
            
            # 保存该类型的完整数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_data(vulnerabilities, f"{vuln_type}_complete_{timestamp}.json")
            
            # 转换为DataFrame并保存为CSV
            if vulnerabilities:
                df = pd.DataFrame(vulnerabilities)
                csv_file = os.path.join(self.data_dir, f"{vuln_type}_vulnerabilities_{timestamp}.csv")
                df.to_csv(csv_file, index=False, encoding='utf-8')
                print(f"{vuln_type}漏洞数据已保存为CSV: {csv_file}")
            
            # 在不同类型之间添加较长的延迟，避免被封
            time.sleep(random.uniform(5, 10))
        
        return all_results

def main():
    crawler = CVEDetailsCrawler()
    
    print("开始爬取各类型Web漏洞数据...")
    all_results = crawler.crawl_all_vulnerability_types(
        start_page=1,
        end_page=5  # 每种类型爬取5页，可以根据需要调整
    )
    
    # 保存所有数据的汇总信息
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_data = {
        'timestamp': timestamp,
        'total_vulnerabilities': sum(len(vulns) for vulns in all_results.values()),
        'vulnerabilities_by_type': {
            vuln_type: len(vulns) for vuln_type, vulns in all_results.items()
        }
    }
    
    crawler.save_data(summary_data, f"crawling_summary_{timestamp}.json")
    print("\n爬取完成！汇总信息已保存。")

if __name__ == "__main__":
    main() 