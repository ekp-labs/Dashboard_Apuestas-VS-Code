import requests
url = 'https://apim.laliga.com/public-service/api/v1/subscriptions/laliga-easports-2026?contentLanguage=en&subscription-key=c13c3a8e2f6b46da9c5c425cf61fab3e'
r = requests.get(url)
data = r.json()
print(data['subscription']['slug'])
# Try to find players endpoint
# Maybe /players? Let's guess
# Common pattern: /players
test_url = 'https://apim.laliga.com/public-service/api/v1/players?subscriptionId=395&contentLanguage=en&subscription-key=c13c3a8e2f6b46da9c5c425cf61fab3e'
r2 = requests.get(test_url)
print(r2.status_code)
print(r2.text[:500])
