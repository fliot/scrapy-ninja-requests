# -*- coding: utf-8 -*-
__version__ = '0.1.0'

import grequests
import json
import random
import requests
from tld import get_tld

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

class ninja_session():
    
    def __init__(self, key=None, proxylist=[], fakeua=True, retry=0, synchr=False, syncpool=5, debug=False):
        self.req = requests.Session()
        self.fakeua = fakeua
        self.retry = retry
        self.preferred = {}
        self.synchr = synchr
        self.syncpool = syncpool
        self.debug = debug
        self.key = key
        if not(self.key is None):
            r = self.req.get(url='https://scrapy.ninja/get_proxy.php?lic=%s' % self.key)
            for i in r.json()['proxies']:
                proxylist.append(i)
        if len(proxylist) == 0: raise Exception('No proxy')
        random.shuffle(proxylist)
        self.proxylist = proxylist
        if self.retry == 0: self.retry = len(self.proxylist)
        if self.debug: print("Proxies loaded (%s)" % len(self.proxylist))
    
    
    def get(self, url, headers={}, timeout=(), accepted_code=[200], unaccepted_strings=[], expected_string=None):
        n = 0
        if timeout == (): timeout = (3.05, 27)
        resultat = None
        preferred = False
        
        proxylist = self.proxylist
        random.shuffle(proxylist)
        fqdn = get_tld(url, as_object=True).fld
        if fqdn in self.preferred.keys():
            proxylist.insert(0, self.preferred[fqdn])
            if self.debug: print("Preferred added (%s)" % self.preferred[fqdn])
        
        if not(self.synchr):
            for i in proxylist[0:self.retry]:
                n += 1
                
                if self.fakeua: headers['User-Agent'] = random.choice(user_agent_list)
                proxies = { "http": "http://%s" % i, "https": "http://%s" % i }
                if self.debug: 
                    print("Attempt %s" % n)
                    print(proxies)
                try:
                    r = self.req.get(url, headers=headers, timeout=timeout, proxies=proxies)
                    accepted = True
                    if r.status_code not in accepted_code:
                        if self.debug: print(f"accepted status code ({r.status_code})")
                        accepted = False
                    for e in unaccepted_strings:
                        if e in r.text:
                            if self.debug: print(f"unaccepted match ({e})")
                            accepted = False
                    if expected_string is not None:
                        if expected_string in r.text:
                            if self.debug: print(f"expected string found ({expected_string})")
                        else:
                            if self.debug: print(f"expected string absent ({expected_string})")
                            accepted = False
                    if accepted:
                        resultat = r
                        self.preferred[fqdn] = i
                        if self.debug: print(self.preferred)
                        break
                except: pass
        else:
            rs = []
            proxylist.reverse()
            for i in self.proxylist[0:self.retry]:
                n += 1
                if self.debug: print("Attempt %s" % n)
                stop = False
                for i in range(self.syncpool):
                    if self.fakeua: headers['User-Agent'] = random.choice(user_agent_list)
                    proxy = proxylist.pop()
                    proxies = { "http": "http://%s" % proxy, "https": "http://%s" % proxy }
                    if self.debug: print(proxies)
                    rs.append(grequests.get(url, headers=headers, timeout=timeout, proxies=proxies))
                res = grequests.map(rs)
                for r in res:
                    try:
                        accepted = True
                        if r.status_code not in accepted_code:
                            if self.debug: print(f"not accepted status code ({r.status_code})")
                            accepted = False
                        else:
                            if self.debug: print(f"ok  accepted status code ({r.status_code})")
                            
                        for e in unaccepted_strings:
                            if e in r.text:
                                if self.debug: print(f"unaccepted match ({e})")
                                accepted = False
                        
                        if expected_string is not None:
                            if expected_string in r.text:
                                if self.debug: print(f"ok  expected string found ({expected_string})")
                            else:
                                if self.debug: print(f"not expected string found ({expected_string})")
                                accepted = False
                        else:
                            if self.debug: print(f"ok  expected string unset")
                        
                        if accepted:
                            stop =True
                            resultat = r
                            if not(preferred):
                                for p in r.connection.proxy_manager.keys():
                                    self.preferred[fqdn] = p.split("/")[-1]
                                    preferred = True
                                if self.debug: print(self.preferred)
                    except: pass
                if stop: break
        
        if self.debug: print("n=%s" % n)
        return resultat
