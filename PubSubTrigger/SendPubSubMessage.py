import requests
import json
import sys


def main(argv):
    print('Publishing Message to Jenkins')

    payload_data = {'value': 'some value data',
                    'value2': 'some more value data',
                    'values': ['a list item 1', 'a list item2']}

    json_payload_data = json.dumps(payload_data, indent=4, sort_keys=True)

    # response = requests.post(url='http://localhost:8080/jenkins/pubsub/publish?message="BuildUpstream"&queryparam="Query param 1"', json=json_payload_data)
    response = requests.post(url='http://192.168.1.11/pubsub/publish?message=BuildUpstream&queryparam="Query param 1"', json=payload_data)
    print(response.text)

if __name__ == '__main__':
    main(sys.argv[1:])
