from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from time import sleep

from loguru import logger as log

# 启动Chrome并附加到现有会话
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
log.info(f"当前URL: {driver.current_url}")


def go_to_site(month: int, day: int, session: int):
    day_str, month_str = str(day).zfill(2), str(month).zfill(2)
    url = f"https://www.cjcf.com.tw/jj01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2024/{month_str}/{day_str}&D2={session}"
    driver.get(url)


def book(index):
    go_to_site(month, day, session)
    element = driver.find_element(By.XPATH, f"//table/tbody/tr[{index}]/td[4]/img")
    element.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    log.info(alert.text)


def book_available(indexes):
    for i in indexes:
        book(i)


month = 7
day = 29
session = 1

runtime = datetime(year=datetime.now().year, month=month, day=day) - timedelta(days=13)

# go_to_site(month, day, session)
while True:
    diff = runtime - datetime.now()
    print(f" \rTime left: {diff}", end="", flush=True)
    if diff > timedelta(seconds=0.0002):
        continue
    try:
        book(7)
        # book(2)
        break
    except Exception as e:
        log.error(e)
