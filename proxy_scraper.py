import requests
from bs4 import BeautifulSoup
import random

# Retrieve and prepare the list of proxies
proxies = []
response = requests.get("https://sslproxies.org/")
soup = BeautifulSoup(response.content, 'html.parser')
proxies_table = soup.find('table', class_='table table-striped table-bordered')
for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
        'ip': row.find_all('td')[0].string,
        'port': row.find_all('td')[1].string
    })

# Create a list of proxy dictionaries
proxies_lst = [{'http': 'http://' + proxy['ip'] + ':' + proxy['port']} for proxy in proxies]



# Function to try requests with different proxies
def try_request_with_proxies(proxies_lst):
    for proxy in proxies_lst:
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
            print(f"Success with proxy: {proxy}")
            return response.json()
        except Exception as e:
            print(f"Failed to connect using proxy {proxy}: {e}")
    raise Exception("All proxies failed")

# Shuffle the list of proxies for random selection
random.shuffle(proxies_lst)

# Try to make the request using the proxies
try:
    result = try_request_with_proxies(proxies_lst)
    print(result)
except Exception as e:
    print(e)
