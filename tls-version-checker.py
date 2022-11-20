# The script only works if you run it in Linux and have tshark installed

import asyncio
import re
import subprocess

PATH_TO_TXT = "test.txt"
PATH_TO_URLS = "URLS.txt"

global tls_versions
tls_versions = []


def get_URLS(path):
    f = open(path, "r")
    urls = f.read().splitlines()
    return urls


async def parse_tls(path):
    tls_versions = []
    f = open(path, "r")
    data = f.read()
    v = re.findall(r"TLSv\S\S\S", data)
    set_v = set(v)
    for i in set_v:
        tls_versions.append([i, v.count(i)])
    tls_versions.sort(key=lambda x: x[1], reverse=True)
    return tls_versions, set_v


async def run_tshark(url, path):
    subprocess.Popen("tshark -Y tls > " + path, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await asyncio.sleep(3)
    subprocess.Popen("curl " + url, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await asyncio.sleep(3)
    subprocess.Popen("pkill tshark", shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await asyncio.sleep(1)
    return


async def get_TLS_info(url, path):
    await run_tshark(url, path)
    v, set_v = await parse_tls(path)
    while len(set_v) == 0:
        await run_tshark(url, path)
        v, set_v = await parse_tls(path)
        await asyncio.sleep(1)
    print("TLS version(s) supported by " + url + " : " + str(v))
    global tls_versions
    tls_versions.append([url, v[0][0]])
    # print("Main " + url + " TLS version : " + str(v[0][0]))
    return

if __name__ == "__main__":
    urls = get_URLS(PATH_TO_URLS)
    for url in urls:
        asyncio.run(get_TLS_info(url, PATH_TO_TXT))
    print(tls_versions)
