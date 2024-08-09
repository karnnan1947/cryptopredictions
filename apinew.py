import requests
import json
api_new=requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
api=json.loads(api_new.content)
print(api['Data'][7]['body'])
