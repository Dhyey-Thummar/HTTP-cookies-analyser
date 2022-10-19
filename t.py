from itertools import dropwhile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = ["https://www.amazon.in/", "https://www.amazon.in/"]

DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
s = Service(DRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = r"C:/Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# options.add_argument(
#     "--user-data-dir=C:\\Users\\dhyey\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default")
# options.add_argument("--profile-directory=Default")
# options.headless = True
driver = webdriver.Chrome(options=options, service=s)

driver.get(url=url[0])
cookies = driver.get_cookies()
print(cookies)
driver.get(url=url[1])
print(driver.get_cookies())
driver.quit()