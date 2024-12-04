import time

from selenium import webdriver
from selenium.webdriver.common.by import By

url = f"https://www.selenium.dev/documentation/webdriver/interactions/alerts/"
driver = webdriver.Chrome()
print('drive!')
driver.get(url=url)
element_alert = driver.find_element(By.LINK_TEXT, f"See a sample confirm")
driver.execute_script("arguments[0].click();", element_alert)
time.sleep(2)
window_alert = driver.switch_to.alert
text = window_alert.text
time.sleep(10)
window_alert.accept()
print(text)

time.sleep(5)

element_alert = driver.find_element(By.LINK_TEXT, f"See a sample confirm")
driver.execute_script("arguments[0].click();", element_alert)
time.sleep(2)
window_alert = driver.switch_to.alert
text = window_alert.text
time.sleep(10)
window_alert.dismiss()
print(text)
