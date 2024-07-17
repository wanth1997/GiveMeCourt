from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta, date
from time import sleep

# 启动Chrome并附加到现有会话
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 确保端口号正确

driver = webdriver.Chrome(options=chrome_options)
print("当前URL: ", driver.current_url)


def go_to_site(month: int, day: int, session: int):
    day_str = str(day).zfill(2)
    month_str = str(month).zfill(2)
    url = f"https://www.cjcf.com.tw/jj01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2024/{month_str}/{day_str}&D2={session}"
    driver.get(url)


def get_available():
    this_block = False
    go_to_site(month, day, session)
    ret = []
    for i in range(2, 22, 5):
        xpath = f"/html/body/table[1]/tbody/tr[3]/td/div/form/table/tbody/tr/td/span/div/table/tbody/tr[2]/td/span/table/tbody/tr[{i}]/td[4]/img"
        element = driver.find_element(By.XPATH, xpath)
        value = element.get_attribute("src")
        if "place01" not in value or this_block:
            continue
        this_block = True
        ret.append(i)
        if len(ret) >= 2:
            return ret
    print(ret)
    return ret


def book_available(indexes):
    for i in indexes:
        go_to_site(month, day, session)
        xpath = f"/html/body/table[1]/tbody/tr[3]/td/div/form/table/tbody/tr/td/span/div/table/tbody/tr[2]/td/span/table/tbody/tr[{i}]/td[4]/img"
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(alert.text)
            alert.accept()

        except Exception as e:
            print(f"An error occurred: {e}")


month = 7
day = 31
session = 3

runtime = datetime(year=datetime.now().year, month=month, day=day) - timedelta(days=13)

go_to_site(month, day, session)
while True:
    diff = runtime - datetime.now()
    print(f" \rTime left: {diff}", end="", flush=True)
    if diff > timedelta(seconds=0):
        sleep(0.01)
        continue
    try:
        go_to_site(month, day, session)
        indexes = [i for i in range(2, 22, 5)]
        book_available(indexes)
        sleep(5)
    except Exception as e:
        print(e)
        sleep(0.01)
        print("Retry!")
