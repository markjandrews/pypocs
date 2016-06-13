import sys
import re
import requests

root_url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php/?nothing='

# Initial
next_nothing = str(16044 / 2)

for i in range(400):
    r = requests.get('%s%s' % (root_url, next_nothing))
    print(r.content)
    sys.stdout.flush()
    next_nothing = re.match(r'^.*?and the next nothing is (.*)$', r.content, flags=re.MULTILINE | re.DOTALL).group(1)

print(next_nothing)
