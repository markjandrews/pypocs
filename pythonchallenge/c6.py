import re
import requests
import zipfile
#
# r = requests.get('http://www.pythonchallenge.com/pc/def/channel.zip')
#
# with open('channel.zip', 'wb') as outf:
#     outf.write(r.content)

next_nothing_file = '90052.txt'
comments = []
with zipfile.ZipFile('channel.zip') as zf:
    for i in range(1000):
        data = zf.read(next_nothing_file)
        print(data)
        try:
            comments.append(zf.getinfo(next_nothing_file).comment)
            next_nothing_file = '%s.txt' % re.match(r'^.*?next nothing is (.*?)$', data,
                                                    flags=re.IGNORECASE | re.DOTALL | re.MULTILINE).group(1)
        except AttributeError:
            break

print("".join(comments))