import time
import random
import json
import pandas as pd
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StockCrawler:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        # 需要无头可以取消注释
        # self.options.add_argument("--headless=new")
        self.driver = None
        self.wait = None
        self.all_data = []

    def init_driver(self):
        """初始化浏览器驱动"""
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 20)

    def wait_for_search_button(self):
        """等待搜索按钮变为可用"""
        for _ in range(20):
            try:
                search_button = self.driver.find_element(By.CSS_SELECTOR, 'div.search-icon')
                if 'search-disable' not in search_button.get_attribute('class'):
                    return search_button
            except:
                pass
            time.sleep(0.5)
        raise Exception("搜索按钮始终不可用")

    def get_robot_data_from_requests(self):
        """从请求中获取数据"""
        for request in self.driver.requests:
            if request.response and 'get-robot-data' in request.url and request.response.status_code == 200:
                try:
                    import gzip
                    response_data = gzip.decompress(request.response.body).decode('utf-8')
                    json_data = json.loads(response_data)
                    # 提取 datas 数据
                    datas = json_data.get('data', {}).get('answer', [])[0].get('txt', [])[0].get('content', {}).get('components', [])[0].get('data', {}).get('datas', [])
                    if datas:
                        self.all_data.extend(datas)
                        print(f"✔ 当前页抓取 {len(datas)} 条记录，累计 {len(self.all_data)} 条")
                    break
                except Exception as e:
                    print("❌ 解析失败：", e)

    def crawl_data(self, query):
        """爬取数据的主函数"""
        try:
            # 打开网页
            self.driver.get("https://www.iwencai.com/unifiedwap/")

            # 输入搜索内容
            search_input = self.wait.until(EC.presence_of_element_located((By.ID, 'searchInput')))
            search_input.clear()
            search_input.send_keys(query)

            # 点击搜索按钮
            search_button = self.wait_for_search_button()
            search_button.click()

            # 等待第一页数据加载完成
            time.sleep(3)
            self.get_robot_data_from_requests()

            # 自动翻页
            page_count = 1
            while True:
                try:
                    next_btn = self.driver.find_element(By.XPATH, "//a[text()='下页']")
                    if next_btn.get_attribute("tabindex") == "-1":
                        print(f"✅ 已到最后一页，共 {page_count} 页，累计 {len(self.all_data)} 条")
                        break
                    else:
                        delay = random.uniform(1, 3)
                        next_btn.click()
                        time.sleep(delay)
                        page_count += 1
                        self.get_robot_data_from_requests()
                except Exception as e:
                    print("⚠️ 找不到下页按钮或其他错误：", e)
                    break

            print(f"\n📊 数据统计：")
            print(f"   - 总页数：{page_count} 页")
            print(f"   - 总记录数：{len(self.all_data)} 条")
            
            # 转换为DataFrame并返回
            return pd.DataFrame(self.all_data)

        except Exception as e:
            print(f"❌ 爬取过程中出错: {str(e)}")
            return pd.DataFrame()

        finally:
            if self.driver:
                self.driver.quit()

def crawl_stock_data(query):
    """便捷的爬取函数"""
    crawler = StockCrawler()
    crawler.init_driver()
    return crawler.crawl_data(query)

def main():
    """主函数，用于测试爬虫功能"""
    # 示例查询
    query = "所有A股"
    print(f"开始爬取数据，查询条件：{query}")
    
    try:
        df = crawl_stock_data(query)
        if not df.empty:
            print("\n数据预览：")
            print(df.head())
            
            # 保存到CSV文件
            output_file = "stock_data.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n数据已保存到：{output_file}")
        else:
            print("未获取到数据")
    except Exception as e:
        print(f"程序执行出错：{str(e)}")

if __name__ == "__main__":
    main() 