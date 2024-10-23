import requests

def get_headers():
  response = requests.get(
    url='https://headers.scrapeops.io/v1/browser-headers',
    params={
        'api_key': 'ef359c6c-468c-4004-8869-da304cbb68dc',
        'num_results': '2'}
  )

  return (response.json())
