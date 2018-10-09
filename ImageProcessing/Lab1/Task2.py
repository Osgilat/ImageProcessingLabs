from PIL import Image
from numpy import *

img = Image.open("forest.bmp")

convertedImg = img.convert ('RGB')

# grab the image dimensions
width = img.size[0]
height = img.size[1]

pixelMap = convertedImg.load()

# loop over the image, pixel by pixel
for x in range(0, width):
    for y in range(0, height):
        pixelRGB = pixelMap[x, y]
        R, G, B = pixelRGB
        brightness = sum([R, G, B]) / 3

        # Set Pixel in new image
        pixelMap[x, y] = (int(brightness), int(brightness), int(brightness))

convertedImg.save("tone.bmp")
convertedImg.show()