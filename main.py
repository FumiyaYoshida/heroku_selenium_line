import time
import os
import requests
# Selenium
from selenium import webdriver
# ChromeDriverのバージョンを合わせるらしい
# import chromedriver_binary
# from webdriver_manager.chrome import ChromeDriverManager
# ページが読み込まれるまで待機するモジュール
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# ChromeDriverのオプション用モジュール
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By

# ドライバーのパス指定
driver_path = '/app/.chromedriver/bin/chromedriver'
# driver_path = "./../chromedriver98"


# Headless Chromeをあらゆる環境で起動させるオプション
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")

#クローラーの起動
chrome_service = fs.Service(executable_path = driver_path)
driver = webdriver.Chrome(service = chrome_service, options = options)

# ページへアクセス
driver.get('https://info.finance.yahoo.co.jp/fx/')
# ページが読み込まれるまでの最大待機時間（10秒）
wait = WebDriverWait(driver, 10)
# ページが読み込まれるまで待機
wait.until(EC.presence_of_all_elements_located)
time.sleep(1)

# ドル円を取得
message = driver.find_element(by=By.XPATH, value="//span[@id='USDJPY_top_bid']").get_attribute("textContent")

# ドライバーを終了させる
driver.close()
driver.quit()
 
# LINE通知用に定義した関数
def line_notify(message):
	line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
	line_notify_api = 'https://notify-api.line.me/api/notify'
	payload = {'message': message}
	headers = {'Authorization': 'Bearer ' + line_notify_token}
	requests.post(line_notify_api, data=payload, headers=headers)
 
 
# LINEに通知させる
line_notify(message)