import PIL
from PIL import Image
from PIL import ImageFilter
import sys
import os
import random
import requests
from io import BytesIO
import math

args = sys.argv

if not len(args) > 1:
    print("Usage: python main.py <image_path> OR python main.py <image_url>")
    sys.exit()

# Get image from url
if args[1].startswith("http"):
    response = requests.get(args[1])
    img = Image.open(BytesIO(response.content))
else:
    if not os.path.isfile(args[1]):
        print("File not found")
        sys.exit()
    img = Image.open(args[1])

# make image black and white
img = img.convert('L')

# make the image square by always stretching
# the shorter side to the length of the longer side
if img.size[0] > img.size[1]:
    img = img.resize((img.size[1], img.size[1]))
else:
    img = img.resize((img.size[0], img.size[0]))

# sharpen image
img = img.filter(ImageFilter.SHARPEN)

# overlay a noise pattern over the image
noise = Image.new('L', img.size, 255)
for x in range(noise.size[0]):
    for y in range(noise.size[1]):
        noise.putpixel((x, y), int(255 * (random.random() ** 2)))

img = Image.blend(img, noise, 0.05)

# add overlay.png to image
overlay = Image.open('overlay.png')
overlay = overlay.resize(img.size)
img.paste(overlay, (0, 0), overlay)

# save image
img.save('output.png')
img.show()

