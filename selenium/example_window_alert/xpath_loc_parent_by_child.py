from selenium import webdriver
from selenium.webdriver.common.by import By


def get_attr(elem, *args):
    return [elem.get_attribute(arg) for arg in args]


driver = webdriver.Chrome()
try:
    driver.get(r"https://www.baidu.com/")
    input_field = driver.find_element(By.XPATH, r'//input[@id="kw"]')

    input_form = input_field.find_element(By.XPATH, r'./parent::*/parent::*')
    input_button = input_field.find_element(By.XPATH, r'./parent::*/following::*[contains(@class, "btn")]//input[@type="submit"]')

    # input_form = driver.find_element(By.XPATH, r'//input[@id="kw"]/../..')
    # input_form = driver.find_element(By.XPATH, r'//input[@id="kw"]/../..')
    print(get_attr(input_form, 'id', 'name', 'action'))
    print(get_attr(input_button, 'type', 'id', 'value'))


finally:
    driver.quit()