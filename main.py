import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def fetch_content_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 运行无头模式
    service = Service(executable_path='')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # 等待JavaScript内容加载
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        content_div = soup.find('div', {'id': 'support_article'})
        return content_div.get_text(strip=True) if content_div else "No content found"
    except Exception as e:
        return f"Error fetching content: {e}"
    finally:
        driver.quit()

def fetch_binance_announcements():
    url = 'https://www.binance.com/zh-TC/support/announcement'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            announcement_container = soup.find('div', class_='css-wrintz')
            if announcement_container:
                announcements = announcement_container.find_all('a', limit=5)  # 提取前5个公告
                for announcement in announcements:
                    title = announcement.get_text()
                    link = 'https://www.binance.com' + announcement['href']
                    print(f'Title: {title}\nLink: {link}')
                    print("Content:\n", fetch_content_with_selenium(link))
                    print("\n-----------------------------\n")
    except Exception as e:
        print('Error:', e)

fetch_binance_announcements()