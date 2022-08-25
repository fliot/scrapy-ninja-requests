# scrapy-ninja-requests
This package provides an enriched [Requests](https://pypi.org/project/requests/) class to use failover rotating proxies, automatically provided within [scrapy.ninja](https://scrapy.ninja/) services subscription.
- rotating proxies
- proxy assignment optimisation
- multi thread (synchr=True & syncpool=5)
- expected http code response control
- retry-able

```
from scrapy_ninja_requests import ninja_session

s = ninja_session(key='KJHGFSERTYUIO87654323ERFGHUIO876543', fakeua=True, country="US", retry=3, synchr=True, syncpool=20)

# once loaded, use it as regular requests.Session:

r = s.get('https://your_www_request', accepted_code=[200,301,302])
print(r.text)
# '......'
```
