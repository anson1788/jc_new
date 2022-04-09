#Simple assignment
from selenium.webdriver import Chrome
driver = webdriver.Chrome('/usr/bin/chromedriver'
#Or use the context manager
from selenium.webdriver import Chrome
with Chrome() as driver:
    url ='https://www.google.com.tw'
    driver.get(url)