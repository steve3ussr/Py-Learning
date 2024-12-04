from selenium import webdriver
import time


driver = webdriver.Chrome()
driver.switch_to.new_window('tab')
time.sleep(5)
driver.close()
driver.switch_to.window(driver.window_handles[-1])
driver.get('https://baidu.com')
driver.save_screenshot('./image.png')
time.sleep(30)
driver.quit()
