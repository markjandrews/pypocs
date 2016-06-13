import requests

requests.packages.urllib3.disable_warnings()

from lxml import html

name = 'userlame'
password = 'daria2hug'

http_proxy = 'http://localhost:8888'
https_proxy = 'https://localhost:8888'
proxy_dict = {
    'http': http_proxy,
    'https': https_proxy
}

session = requests.Session()
r = session.get('https://microcorruption.com/login', proxies=proxy_dict, verify=False)

tree = html.fromstring(r.content)
data_dict = {'authenticity_token': tree.xpath('//meta[@name="csrf-token"]/@content')[0],
             'name': name,
             'password': password}

print('Logging in token: %s' % data_dict['authenticity_token'])

r = session.post('https://microcorruption.com/login', data=data_dict, proxies=proxy_dict, verify=False)
tree = html.fromstring(r.content)

authenticity_token = tree.xpath('//meta[@name="csrf-token"]/@content')[0]
print('API Token: %s' % authenticity_token)

session.headers.update({'X-CSRF-Token': authenticity_token})

r = session.get('https://microcorruption.com/get_levels', data=data_dict, proxies=proxy_dict, verify=False)
levels = r.json()
print(levels)

data_dict = {"body": {}}
r = session.post('https://microcorruption.com/cpu/is_alive', json=data_dict, proxies=proxy_dict, verify=False)
print(r.content)

data_dict = {"body": {"level": "Sydney"}}
r = session.post('https://microcorruption.com/cpu/set_level', json=data_dict, proxies=proxy_dict, verify=False)
print(r.content)

# Logout
r = session.get('https://microcorruption.com/logout', data=data_dict, proxies=proxy_dict, verify=False)
print(r.content)
# result = r.json()
# print(result)
