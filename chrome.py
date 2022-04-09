#Simple assignment
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
chrome_options = Options("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=chrome_options)
#Or use the context manager
with Chrome() as driver:
    url ='https://www.google.com.tw'
    driver.get(url)

