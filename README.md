# Wencai Stock Data Collector

一个用于从同花顺问财获取数据的工具。

## 功能特点

- 支持自定义查询条件
- 自动翻页获取数据
- 数据导出为DataFrame格式
- 内置反爬虫措施

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```python
from stock_crawler import crawl_stock_data

# 示例：查询所有A股
df = crawl_stock_data("所有A股")
print(df)
```

## 注意事项

- 使用前请确保已安装Chrome浏览器
- 需要安装对应版本的ChromeDriver
- 建议适当控制爬取频率，避免被封IP 
