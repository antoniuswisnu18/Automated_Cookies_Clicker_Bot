import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:/Users/user/Downloads/Programs/chromedriver_win32/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get(url="https://orteil.dashnet.org/experiments/cookie/")
cookie_obj = driver.find_element(By.ID, "cookie")

items_content = driver.find_elements(By.CSS_SELECTOR, "#rightPanel #store div")
items_id = [item.get_attribute("id") for item in items_content]


break_time = time.time() + 5
timeout = time.time() + 60

while time.time() < timeout:
    cookie_obj.click()
    if time.time() > break_time:
        money_text = driver.find_element(By.ID, "money").text
        if "," in money_text:
            money_text = money_text.replace(",", "")
        money = int(money_text)

        prices_content = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = []
        for x in prices_content:
            price_text = x.text
            if price_text != "":
                price = int(price_text.replace(" ","").split("-")[1].replace(",",""))
                prices.append(price)

        all_upgrades = {}
        for x in range(len(prices)):
            all_upgrades[prices[x]] = items_id[x]

        avail_upgrades = {}
        for price, id in all_upgrades.items():
            if money > price:
                avail_upgrades[price] = id

        current_upgrade_price = max(avail_upgrades)
        current_upgrade_id = avail_upgrades[current_upgrade_price]

        driver.find_element(By.ID, current_upgrade_id).click()

        break_time = time.time() + 5

cookie_per_sec = driver.find_element(By.ID, "cps").text
print(cookie_per_sec)
