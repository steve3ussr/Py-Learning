from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import json


def click(d, elem: WebElement) -> None:
    try:
        elem.click()
    except ElementClickInterceptedException:
        d.execute_script("arguments[0].click();", elem)
    except Exception as e:
        print(f"Unexpected exception when clicking element: {e}")
        raise e


def main():
    driver = webdriver.Chrome()
    assert driver is not None
    driver.maximize_window()

    try:
        driver.get('https://www.bilibili.com')
        driver.implicitly_wait(5)
        driver.refresh()
        driver.implicitly_wait(5)

        # multiple methods to locate element
        # button_msg = driver.find_element(By.XPATH, '//div[@data-idx="message"]')
        button_msg = driver.find_element(By.XPATH, '// span[contains(text(), "消息")]')

        click(driver, button_msg)

        time.sleep(360)

    except KeyboardInterrupt:
        pass

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
