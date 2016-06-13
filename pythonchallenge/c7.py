import requests
from PIL import Image
#
# r = requests.get('http://www.pythonchallenge.com/pc/def/oxygen.png')
# with open('oxygen.png', 'wb') as outf:
#     outf.write(r.content)

with open('oxygen.png', 'rb') as inf:
    img = Image.open(inf)
    row = img.size[1] / 2
    pixels = [img.getpixel((x, row)) for x in range(0, 629, 7)]

pixels = [r for r, g, b, a in pixels if r == g == b]
letters = [chr(x) for x in pixels]
print(''.join(letters))
print(''.join(chr(x) for x in [105, 110, 116, 101, 103, 114, 105, 116, 121]))
