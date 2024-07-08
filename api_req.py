import requests
from bs4 import BeautifulSoup

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
print(proxies_lst)

