import os
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

pathOutput = "output.txt"
pathExcel = "cookie-db.xlsx"
PATH_TO_URLS = "URLS.txt"

DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
s = Service(DRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = r"C:/Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# options.add_argument(
#     "--user-data-dir=C:\\Users\\dhyey\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default")
# options.add_argument("--profile-directory=Default")
options.add_argument("--log-level=3")
options.headless = True
driver = webdriver.Chrome(options=options, service=s)


def getAllurls(path):
    with open(path, 'r') as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    return urls


def getAllParams(driver, urls):
    cookies = []
    for url in urls:
        print('Getting cookies for: ' + url)
        try:
            driver.get(url=url)
            cookies.append(driver.get_cookies())
            driver.implicitly_wait(3)
        except Exception as e:
            print(e)
    # print(cookies)
    paramList = []
    c = 0
    for cookie in cookies:
        params = {'url': urls[c], 'name': [], 'value': [], 'domain': [], 'path': [],
                  'expires': [], 'httpOnly': [], 'secure': [], 'sameSite': []}
        for i in cookie:
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
        paramList.append(params)
        c += 1

    return paramList


def printCookieTable(paramList, urls):
    if os.path.exists(pathOutput):
        os.remove(pathOutput)
    for i in range(len(paramList)):
        params = paramList[i]
        table = pt.PrettyTable()
        table.title = 'Cookies for: ' + urls[i]
        table.field_names = ['Name', 'Value', 'Domain',
                             'Path', 'Expires', 'HttpOnly', 'Secure', 'SameSite']
        table.align = 'l'
        table.max_width = 40
        for i in range(len(params['name'])):
            table.add_row([params['name'][i], params['value'][i], params['domain'][i], params['path'][i],
                          params['expires'][i], params['httpOnly'][i], params['secure'][i], params['sameSite'][i]])

        with open(pathOutput, 'a') as f:
            f.write(table.get_string())
            f.write('\n\n')
        print(table)
        print()


def SaveToExcel(paramList, urls):
    if os.path.exists(pathExcel):
        os.remove(pathExcel)
    df_main = pd.DataFrame()
    for i in range(len(paramList)):
        params = paramList[i]
        df = pd.DataFrame(params)
        df_main = pd.concat([df_main, df], ignore_index=True)
    df_main.to_excel(pathExcel, index=False)


if __name__ == '__main__':
    urls = getAllurls(PATH_TO_URLS)
    params = getAllParams(driver, urls)
    # printCookieTable(params, urls)
    SaveToExcel(params, urls)
