# 要用sudo启动


from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

driver.find_element("hello")
