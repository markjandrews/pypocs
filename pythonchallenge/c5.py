import requests
import pickle
import sys


r = requests.get('http://www.pythonchallenge.com/pc/def/banner.p')

obj = pickle.loads(r.content)

for line in obj:
    print(''.join(item[0]*item[1] for item in line))