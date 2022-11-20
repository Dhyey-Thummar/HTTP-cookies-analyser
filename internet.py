import time
from selenium import webdriver
import sys
import getpass
from selenium.webdriver.chrome.service import Service

username = sys.argv[1]
password = getpass.getpass()


DRIVER_PATH = "~/chromedriver"
s = Service(DRIVER_PATH)
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--whitelisted-ips')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.binary_location = r"C:/Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
d = webdriver.Chrome(options=chrome_options, port=3000, service=s)
d.get('https://internet.iitgn.ac.in/')
time.sleep(3)
d.get_screenshot_as_file('1a.png')
time.sleep(3)
uname = d.find_element("id","LoginUserPassword_auth_username")
uname.send_keys(username)
upass = d.find_element("id", "LoginUserPassword_auth_password")
upass.send_keys(password)
button = d.find_element("id", "UserCheck_Login_Button_span")
button.click()
time.sleep(2)
d.get_screenshot_as_file('1b.png')
