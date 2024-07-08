import http.client

conn = http.client.HTTPSConnection("amazon-scrapper17.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "be8ccbb9e0msh5115a6033bee5b6p105708jsn81d7946d1afe",
    'x-rapidapi-host': "amazon-scrapper17.p.rapidapi.com"
}

conn.request("GET", "/products/B0953MCTTQ/reviews?apiKey=3c801d11ddb8472ee82c78036719fd15", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))