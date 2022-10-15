import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import sys

URLS = []  # URL is the masterlist containing all the links


class Links:  # To find and store the links in Site.txt

    def __init__(self, url) -> None:
        self.linktosite = url

    def findalllinks(self):  # fxn to find all the links of that site
        try:
            reqs = requests.get(self.linktosite)
        except:
            s = "URL - "+self.linktosite+" refused to connect!"
        else:
            soup = BeautifulSoup(reqs.text, 'html.parser')
            for link in soup.find_all('a'):
                try:
                    l = link.get('href')
                    if l in URLS:
                        continue
                    else:
                        if l.startswith("http"):
                            URLS.append(l)
                        else:
                            l = self.linktosite+l
                            if l in URLS:
                                continue
                            else:
                                URLS.append(l)
                except:
                    pass
            with open('Site.txt', "a", encoding='UTF-8') as f:
                for link in URLS:
                    f.write(link)
                    f.write("\n")
            s = "Connected Successfully"
        return s

    def BasicInfo(self):

        try:
            r = requests.get(self.linktosite)
        except:
            info = "URL - "+self.linktosite+" refused to connect!"
        else:
            info = {
                'url': "",
                'protocol': "",
                'date': "",
                'status': "",
                'server': "Not Specified",
                'age': "Not Specified",
                'expires': "Not Specified"
            }

            info['url'] = r.url
            p = r.url.split(":")
            info['protocol'] = p[0].upper()

            if "date" in r.headers:
                info['date'] = "Request sent at "+str(r.headers['date'])

            x = r.status_code
            # ADD MORE STATUS CODE RESPONSES HERE
            if x == 200:
                info['status'] = "Request executed successfully!"
            elif x == 301:
                info['status'] = "Redirecting you"
            elif x == 404:
                info['status'] = "Page not found - Bad Request!"

            if "server" in r.headers:
                info['server'] = "Request handled by server " + \
                    str(r.headers['server'])

            if "age" in r.headers:
                info['age'] = "The document has been in your proxy cache since " + \
                    str(r.headers['age']+" seconds")

            if "expires" in r.headers:
                if r.headers['expires'] == '-1':
                    info['expires'] = 'Response wont expire'
                else:
                    info['expires'] = "Response wl be considered expired at " + \
                        str(r.headers['expires'])
            # else:
                #print("Document has no expiry!")
                # if expires not in hlist does that mean ke next time i go to the same link and if present in cache, it will display me the same document?

        return info

    def PrintInfo(self):

        info = self.BasicInfo()

        if "refused" in info:
            print("Connection refused by ", self.linktosite)
            with open('Output123.txt', "a", encoding='UTF-8') as f:
                f.write(info)
                f.write("\n\n")
        else:
            print("Connected successfully to ", self.linktosite)
            BasicParameters = PrettyTable()
            BasicParameters.field_names = ['Parameters', 'Values']
            BasicParameters.add_row(['Site Address', info['url']])
            BasicParameters.add_row(['Protocol', info['protocol']])
            BasicParameters.add_row(['Date & Time of Request', info['date']])
            BasicParameters.add_row(['Request Status', info['status']])
            BasicParameters.add_row(['Name of Server', info['server']])
            BasicParameters.add_row(['Age', info['age']])
            BasicParameters.add_row(['Expires', info['expires']])

            with open('Output123.txt', "a", encoding='UTF-8') as f:
                f.write(str(BasicParameters))
                f.write("\n\n")


class Security:

    def __init__(self, url) -> None:
        self.linktosite = url

    def ANALYZE_COOKIE(self):
        try:
            r = requests.get(self.linktosite)
        except:
            cookies = "URL - "+self.linktosite+" Failed to establish connection"
        else:
            cookies = {
                'name': [],
                'value': [],
                'domain': [],
                'path': [],
                'expiry': [],
                'secure': [],
                'httponly': [],
                'samesite': []
            }
            for c in r.cookies:
                cookies['name'].append(c.name)
                cookies['domain'].append(c.domain)
                cookies['path'].append(c.path)
                cookies['value'].append(c.value)
                cookies['secure'].append(c.secure)
                attributes = c._rest

                if 'HttpOnly' in attributes:
                    cookies['httponly'].append('Yes')
                else:
                    cookies['httponly'].append("No")

                if 'SameSite' in attributes:
                    cookies['samesite'].append(attributes['SameSite'])
                else:
                    cookies['samesite'].append('Lax')  # Default behaviour

            x = r.raw.headers.getlist('Set-Cookie')
            for j in x:
                if 'expires' in j:
                    s = j.find('expires')
                    if j[s+8:s+10] != -1:
                        cookies['expiry'].append(j[s+8:s+37])
                    else:
                        cookies['expiry'].append("No expiry")
                else:
                    cookies['expiry'].append("No expiry")
        return cookies

    def PRINT_COOKIE(self):

        cookies = self.ANALYZE_COOKIE()

        if cookies == ("URL - "+self.linktosite+" Failed to establish connection"):
            with open('Output123.txt', "a", encoding='UTF-8') as f:
                f.write("\n")
                f.write(cookies)
                f.write("\n")

        else:
            with open('Output123.txt', "a", encoding='UTF-8') as f:
                if len(cookies['name']) == 0:
                    f.write("\nNo cookies in the site\n")
                else:
                    cookietable = PrettyTable()
                    cookietable.field_names = [
                        'Name', 'Secure', 'Safe from Javascript?', 'Accessible to other sites?']
                    for i in range(len(cookies['name'])):
                        cookietable.add_row(
                            [cookies['name'][i], cookies['secure'][i], cookies['httponly'][i], cookies['samesite'][i]])
                    f.write(
                        "\nThe summary of all the cookies generated in the site is as follows: \n")
                    f.write(str(cookietable))

                    for i in range(len(cookies['name'])):
                        f.write("\n\nName of cookie: "+cookies['name'][i])
                        f.write("\n")

                        vulnerabilities = []
                        perfect = []
                        recommendations = []

                        if cookies['secure'][i] == True:
                            perfect.append(
                                "Cookies will be transferred only over HTTPS! - You are safe")
                        else:
                            vulnerabilities.append(
                                "Cookies not being transferred over HTTPS! - Might be exploited")
                            recommendations.append(
                                "Set Secure flag in cookies")

                        if cookies['httponly'][i] == 'No':
                            vulnerabilities.append(
                                "Cookies accessible to Javascript code - prone to XSS Vulnerability")
                            recommendations.append(
                                "Set HttpOnly flag in cookies")
                        else:
                            perfect.append(
                                "Cookies not accessible to Javascript - You are safe")

                        if cookies['samesite'][i] == 'Lax':
                            perfect.append(
                                'Accessible till the origin of the site')
                        elif cookies['samesite'][i] == 'Strict':
                            perfect.append('Accessible only to that site')
                        else:
                            vulnerabilities.append(
                                'Cookies are accessible even in cross-requests - can be exploited')
                            recommendations.append(
                                'Set SameSite flag to Lax or Strict')

                        if len(perfect) > 0:
                            f.write("\nFollowing features were found safe: \n")
                            for properties in perfect:
                                f.write(properties)
                                f.write("\n")
                        f.write("\n")

                        if len(vulnerabilities) > 0:
                            f.write(
                                "\nFollowing features were found vulnerable\n")
                            cAnalysis = PrettyTable()
                            cAnalysis.field_names = [
                                'Vulnerabilities', 'Recommendations']
                            for n in range(len(vulnerabilities)):
                                cAnalysis.add_row(
                                    [vulnerabilities[n], recommendations[n]])
                            f.write(str(cAnalysis))
                            f.write("\n")

    def SITE_ANALYSIS(self):

        try:
            r = requests.get(self.linktosite)
        except:
            X = "URL - "+self.linktosite+" Failed to establish connection"
        else:
            X = {
                'frame-options': '',
                'XSS-protection': '',
                'Content-type':  '',
                'Strict-Transport-Security': ""
            }
            try:
                s1 = r.headers['X-Frame-Options']
                X['frame-options'] = r.headers['X-Frame-Options']
            except:
                X['frame-options'] = "None"

            try:
                s2 = r.headers['X-XSS-Protection']
                X['XSS-protection'] = r.headers['X-XSS-Protection']
            except:
                X['XSS-protection'] = '0'

            try:
                s3 = r.headers['X-Content-Type-Options']
                X['Content-type'] = r.headers['X-Content-Type-Options']
            except:
                X['Content-type'] = "None"

            try:
                s4 = r.headers['strict-transport-security']
                X['Strict-Transport-Security'] = r.headers['strict-transport-security']
            except:
                X['Strict-Transport-Security'] = False

        return X

    def PRINT_SITEANALYSIS(self):

        X = self.SITE_ANALYSIS()
        if X == ("URL - "+self.linktosite+" Failed to establish connection"):
            with open('Output123.txt', "a", encoding='UTF-8') as f:
                f.write("\n")
                f.write(X)
                f.write("\n")

        else:
            with open('Output123.txt', "a", encoding='UTF-8') as f:
                sitetable = PrettyTable()
                f.write("\nAnalysis of site is as follows: ")
                sitetable.field_names = [
                    'Frame-Options', 'XSS-Protection', 'Content-Type-Options', 'Strict-Transport-Security']
                sitetable.add_row([X['frame-options'], X['XSS-protection'],
                                  X['Content-type'], X['Strict-Transport-Security']])
                f.write("\n")
                f.write(str(sitetable))

                Sitevulnerabilities = []
                Siteperfect = []
                Siterecommendations = []

                # aa je headers na responses hoy like SAMEORIGIN they are all in capitals in every website right???
                if X['frame-options'] == 'SAMEORIGIN':
                    Siteperfect.append(
                        "Sites except for origin site wont be able to load your webpage in frame/i-frame")
                elif X['frame-options'] == 'DENY':
                    Siteperfect.append(
                        "No Sites (not even origin) will be able to load your webpage in frame/i-frame")
                else:
                    Sitevulnerabilities.append(
                        "The webpage can be loaded in another site as frame element - chance of Clickjacking attack")
                    Siterecommendations.append(
                        "Please set X-Frame-Options either as DENY or SAMEORIGIN")

                if X['XSS-protection'] == '0':
                    # These protections are largely unnecessary in modern browsers when sites implement a strong Content-Security-Policy that disables the use of inline JavaScript ('unsafe-inline').
                    Sitevulnerabilities.append(
                        "XSS Cross scripting attack is possible!")
                    Siterecommendations.append(
                        "Please set X-XSS-Protection bit as 1 and mode=block or report=<reporting-URI>")
                    # report=<reporting-URI> uses the functionality of the CSP report-uri directive to send a report.
                # else:
                    # https://stackoverflow.com/questions/9090577/what-is-the-http-header-x-xss-protection#:~:text=In%20the%20end%2C%20if%20your,browser%20that%20supports%20this%20feature.

                if X['Content-type'] == 'None':
                    Sitevulnerabilities.append(
                        "It will allow browser to sniff the format of uploaded file and if it differs with Accepted format, priority will be given to browser sniff")
                    Siterecommendations.append(
                        "Please set X-Content-Type as nosniff")
                else:
                    Siteperfect.append(
                        "X-Content-Type is nosniff, which will prevent browser from executing an uploaded file format different than specified")

                if X['Strict-Transport-Security'] == False:
                    Sitevulnerabilities.append(
                        "If user wont manually type https, browser will communicate over http protocol, leaving user vulnerable")
                    Siterecommendations.append(
                        "Please set X-strict-transport-security as true, max-age=1 year and include sub-domains")
                else:
                    sts = X['Strict-Transport-Security']
                    if 'includeSubDomains' in sts:
                        Siteperfect.append(
                            "All communication is secure inspite of user not typing https")
                    else:
                        Sitevulnerabilities.append(
                            "STS Applicable only for this site and not for subdomains!")
                        Siterecommendations.append(
                            "Please set include subdomains in X-strict-transport-security")

                if len(Siteperfect) > 0:
                    f.write("\n\nFollowing features were found safe: \n")
                    for properties in Siteperfect:
                        f.write(properties)
                        f.write("\n")
                    f.write("\n")

                if len(Sitevulnerabilities) > 0:
                    f.write("\n\nFollowing features were found vulnerable\n")
                    sAnalysis = PrettyTable()
                    sAnalysis.field_names = [
                        'Vulnerabilities', 'Recommendations']
                    for n in range(len(Sitevulnerabilities)):
                        sAnalysis.add_row(
                            [Sitevulnerabilities[n], Siterecommendations[n]])
                    f.write(str(sAnalysis))
                    f.write("\n\n")

    def Content_Security_Policy(self):
        try:
            r = requests.get(self.linktosite)
        except:
            temp = "temp"
        else:
            s = r.headers['Content-Security-Policy']
            x = s.split("; ")
            # missing base-uri
            # setting script-src value to *
            scriptpresent = False
            for i in x:
                if 'script-src' in i:
                    print("script-src has been explicitly mentioned")
                    scriptpresent = True
                    y = i.split(" ", 1)
                    if 'unsafe-inline' in y[1]:
                        if 'nonce' in y[1]:
                            print("unsafe-inline is ignored coz nonce is present")
                        else:
                            print(
                                "WARNING -'unsafe-inline' allows the execution of unsafe in-page scripts and event handlers.")
                    if 'unsafe-eval' in y[1]:
                        if 'nonce' in y[1]:
                            print("unsafe-eval is ignored coz nonce is present")
                        else:
                            print(
                                "WARNING -'unsafe-eval' allows the execution of code injected into DOM APIs such as eval().")
                    if 'data' in y[1]:
                        print(
                            "DANGER - an attacker can also inject arbitrary data: URIs.")
                    if ((('http' in i) or ('https' in y[1])) and 'strict-dynamic' not in y[1]):
                        print(
                            "WARNING -'unsafe-inline' allows the execution of unsafe in-page scripts and event handlers.")
                    if '*' in y[1]:
                        print("DANGEROUS - script being allowed access from anywhere")
                if 'frame-ancestors' in i:
                    y = i.split(" ", 1)
                    if len(y) > 1:
                        if y[1] == 'self' or y[1] == 'none':
                            print("SAFE MODE")
                        else:
                            print(
                                "The list of sites that can frame given site is: ", y[1])
                    else:
                        print("SAFE MODE!")
                if 'object-src' in i:
                    print("object-src has been explicitly mentioned")
                    y = i.split(" ", 1)
                    if 'none' in y[1]:
                        print(
                            " Prevents fetching and executing plugin resources embedded using <object>, <embed> or <applet> tags. ")
                    elif 'self' in y[1]:
                        print(
                            "Allows fetching and executing plugin resources embedded using <object>, <embed> or <applet> tags only from origin")
                        print("If not required, please restrict object-src to none!")
                    else:
                        print("SEVERELY VULNERABLE - allows ")
            if scriptpresent == False:
                print(
                    "WARNING - you havent specified the source of scripts - threat of XSS")


def final():
    n = len(sys.argv)
    try:
        url = sys.argv[1]
    except:
        print("Please pass a link as argument and also type -d if you also wish to analyze the subsites")
    else:
        L = Links(url)
        # s = L.findalllinks()
        print("Analysing Link")
        if True:
            print("Finding sublinks")
            with open('Site.txt', "r", encoding='UTF-8') as f1:
                links = f1.read().split("\n")
                # links.remove("")

        try:
            detail = sys.argv[2]
        except:
            detail = None
        if detail == "-d":
            for link in links:
                L = Links(link)
                L.PrintInfo()
                S = Security(link)
                S.PRINT_COOKIE()
                S.PRINT_SITEANALYSIS()
        else:
            L = Links(url)
            L.PrintInfo()
            S = Security(url)
            S.PRINT_COOKIE()
            S.PRINT_SITEANALYSIS()


final()
