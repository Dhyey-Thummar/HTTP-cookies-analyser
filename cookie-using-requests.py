import prettytable as pt
import requests


def getAllParams(url):
    request = requests.get(url)
    status = request.status_code
    print('Status: ' + str(status))
    cookies = request.cookies

    params = {'name': [], 'value': [], 'domain': [], 'path': [],
              'expires': [], 'httpOnly': [], 'secure': [], 'sameSite': []}

    for i in cookies:
        params['name'].append(i.name)
        params['value'].append(i.value)
        params['domain'].append(i.domain)
        params['path'].append(i.path)
        params['expires'].append(i.expires)
        params['httpOnly'].append(i.has_nonstandard_attr('HttpOnly'))
        params['secure'].append(i.has_nonstandard_attr('Secure'))
        params['sameSite'].append(i.has_nonstandard_attr('SameSite'))

    return params


def printCookieTable(params, url):
    table = pt.PrettyTable()
    table.title = 'Cookies for: ' + url
    table.field_names = ['Name', 'Value', 'Domain',
                         'Path', 'Expires', 'HttpOnly', 'Secure', 'SameSite']
    table.align = 'l'
    table.max_width = 50
    for i in range(len(params['name'])):
        table.add_row([params['name'][i], params['value'][i], params['domain'][i], params['path'][i],
                      params['expires'][i], params['httpOnly'][i], params['secure'][i], params['sameSite'][i]])

    with open('cookies.txt', 'w') as f:
        f.write(table.get_string())
    print(table)


if __name__ == '__main__':
    url = input('Enter URL: ')
    params = getAllParams(url)
    printCookieTable(params, url)
