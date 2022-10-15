from xmlrpc.client import Server
import requests
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
s = Service(DRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = r"C:/Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options.add_argument(
    "--user-data-dir=C:\\Users\\dhyey\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default")
options.add_argument("--profile-directory=Default")
# options.headless = True
driver = webdriver.Chrome(options=options, service=s)


def getAllParams(chromedriver, URL):
    chromedriver.get(url=URL)
    cookies = chromedriver.get_cookies()
    print(cookies)
    params = {'name': [], 'value': [], 'domain': [], 'path': [],
              'expires': [], 'httpOnly': [], 'secure': [], 'sameSite': []}

    for i in cookies:
        params['name'].append(i['name'])
        params['value'].append(i['value'])
        params['domain'].append(i['domain'])
        params['path'].append(i['path'])
        params['expires'].append(
            i['expiry']) if 'expiry' in i else params['expires'].append(None)
        params['httpOnly'].append(i['httpOnly'])
        params['secure'].append(i['secure'])
        params['sameSite'].append(
            i['sameSite']) if 'sameSite' in i else params['sameSite'].append('')
        chromedriver.quit()
    return params


def printCookieTable(params, url):
    table = pt.PrettyTable()
    table.title = 'Cookies for: ' + url
    table.field_names = ['Name', 'Value', 'Domain',
                         'Path', 'Expires', 'HttpOnly', 'Secure', 'SameSite']
    table.align = 'l'
    table.max_width = 40
    for i in range(len(params['name'])):
        table.add_row([params['name'][i], params['value'][i], params['domain'][i], params['path'][i],
                      params['expires'][i], params['httpOnly'][i], params['secure'][i], params['sameSite'][i]])

    with open('cookies.txt', 'w') as f:
        f.write(table.get_string())
    print(table)


if __name__ == '__main__':
    # url = input('Enter URL: ')
    url = 'https://ims.iitgn.ac.in/student/RequestStatusView.aspx'
    params = getAllParams(driver, url)
    printCookieTable(params, url)
