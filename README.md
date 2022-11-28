# HTTP-cookies-analyser

This is a simple tool to analyse HTTP cookies. It is written in Python.

## Contents

- [`cookie-scraper.py`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/cookie-scraper.py) - This is the main script. It is used to scrape cookies from a website using the Selenium library. It reads URLs from [`URLS.txt`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/URLS.txt) and stores the cookies in [`cookie-db.xlsx`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/cookie-db.xlsx).

- [`cookie-using-requests.py`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/cookie-using-requests.py) - This script is used to scrape cookies from a website using the requests module and just prints them. [Deprecated]

- [`tls-version-checker.py`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/tls-version-checker.py) - This script is used to check the TLS version of a website. It reads URLs from `URLS.txt` and prints the TLS version of each website.

- [`ARP_Spoofer.py`](https://github.com/Dhyey-Thummar/HTTP-cookies-analyser/blob/master/ARP_Spoofer.py) - This script is an attempted demo ARP Spoof attack from one host in IITGN network to a victim in the same network. We observed that the basic attack fails possibly due to preventive measures at the DHCP Server or checks configured into the Ethernet switches. More advanced  MITM techniques may be needed to make the attack successful.

- Rest of the files are just for testing and are not used in the main code. The `.xlsx` files are the database of cookies. The `URLS-xx.txt` contains different URLS. The `chromedriver_win32` directory is the driver necessary for Selenium to run for the `cookie-scraper.py` script.

## Usage

- Install the required libraries using `pip install -r requirements.txt`.

- Run the `cookie-scraper.py` script by `python cookie-scraper.py`.

- Run the `tls-version-checker.py` script by `sudo python tls-version-checker.py`. [ Note: The script needs to run in Linux environment and requires `tshark` module to be installed. Also, needs to be run as root because it uses the `socket` module. ]

- Run the 'ARP_Spoofer.py' script by 'python ARP_Spoofer.py' command and check change (or no change) in ARP Table entries using 'arp -a' command

## Dependencies

- Python 3
- Selenium
- Requests [Deprecated]
- Pandas
- PrettyTable
- Tshark (for `tls-version-checker.py`)
- Scapy (for `ARP_Spoofer.py`)
