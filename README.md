# scrapy-ninja-requests
This package provides an enriched [Requests](https://pypi.org/project/requests/) class to use failover rotating proxies.

```
from scrapy_ninja_requests import requests

s = requests.Session(key='KJHGFSERTYUIO87654323ERFGHUIO876543', fakeuseragent=True, retry=3)

# once loaded, use it as regular requests.Session:

r = s.get('https://your_www_request')
print(r.text)
# '......'
```
