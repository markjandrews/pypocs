import requests
from bs4 import BeautifulSoup

response = requests.get('http://localhost:42684/Main.aspx')

soup = BeautifulSoup(response.content)

payload = {}

for input in soup.find_all('input'):
    name = input.get('name')
    value = input.get('value')
    payload[name] = value

    # if 'Button1' in name:
    #     print(input)

payload['txtBox1'] = "This is going to be the test!"

response = requests.post('http://localhost:42684/Page2.aspx', data=payload)

for input in soup.find_all('input'):
    name = input.get('name')
    value = input.get('value')
    payload[name] = value

    print(input)
    # if '__VIEWSTATE' in name:
    #     break

    input = None

if input is None:
    print('State not found')
    exit(0)

state_data = value.decode('base64')
print(state_data)
