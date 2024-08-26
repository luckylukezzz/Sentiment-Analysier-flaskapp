import requests
from bs4 import BeautifulSoup
import random

def scrape_proxies():
    proxies = []
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html.parser')
    proxies_table = soup.find('table', class_='table table-striped table-bordered')
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    proxies_lst = [{'http': 'http://' + proxy['ip'] + ':' + proxy['port']} for proxy in proxies]
    return proxies_lst

def get_working_proxies():
    proxies_lst = scrape_proxies()
    working_proxies=[]
    for proxy in proxies_lst:
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
            working_proxies.append(proxy)
        except Exception as e:
            print(f"Failed to connect using proxy {proxy}: {e}")
    return working_proxies


print(get_working_proxies())