import requests
from bs4 import BeautifulSoup
import random

response = requests.get(
  url='https://headers.scrapeops.io/v1/browser-headers',
  params={
      'api_key': 'ef359c6c-468c-4004-8869-da304cbb68dc',
      'num_results': '1'}
)

scrape_headers = response.json()
print(scrape_headers)

url ="https://www.amazon.com//dp/B0CWS8MNW1"
response = requests.get(url, headers=scrape_headers["result"][0]  )

# , proxies= {'http': 'http://124.6.155.170:3131'}

print(response.status_code)
print(response.text)


