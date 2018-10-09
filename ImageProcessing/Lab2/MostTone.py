import numpy as numpy
from PIL import Image

img = Image.open("forest.bmp")

convertedImg = img.convert('RGB')

# grab the image dimensions
width = img.size[0]
height = img.size[1]

pixelMap = convertedImg.load()
newimg = Image.new("RGB", (width, height), "white")

def average(times):
    N = float(len(times))
    return (sum(t[0] for t in times)/N,
            sum(t[1] for t in times)/N,
            sum(t[2] for t in times)/N)

for x in range(2, width - 1, 1):
    for y in range(2, height - 1, 1):

        neighbours = numpy.array(
            [pixelMap[x - 1, y - 1], pixelMap[x - 1, y], pixelMap[x - 1, y + 1],
             pixelMap[x, y - 1], pixelMap[x, y], pixelMap[x, y + 1],
             pixelMap[x + 1, y - 1], pixelMap[x + 1, y], pixelMap[x + 1, y + 1]])

        mean1 = average([pixelMap[x - 1, y - 1], pixelMap[x - 1, y],
                            pixelMap[x, y - 1], pixelMap[x, y]])

        mean2 = average([pixelMap[x - 1, y], pixelMap[x - 1, y + 1],
                            pixelMap[x, y], pixelMap[x, y + 1]])

        mean3 = average([pixelMap[x, y - 1], pixelMap[x, y],
                            pixelMap[x + 1, y - 1], pixelMap[x + 1, y]])

        mean4 = average([pixelMap[x, y], pixelMap[x, y + 1],
                            pixelMap[x + 1, y], pixelMap[x + 1, y + 1]])

        dispersion1 = numpy.std([pixelMap[x - 1, y - 1], pixelMap[x - 1, y],
                                 pixelMap[x, y - 1], pixelMap[x, y]])

        dispersion2 = numpy.std([pixelMap[x - 1, y], pixelMap[x - 1, y + 1],
                                 pixelMap[x, y], pixelMap[x, y + 1]])

        dispersion3 = numpy.std([pixelMap[x, y - 1], pixelMap[x, y],
                                 pixelMap[x + 1, y - 1], pixelMap[x + 1, y]])

        dispersion4 = numpy.std([pixelMap[x, y], pixelMap[x, y + 1],
                                 pixelMap[x + 1, y], pixelMap[x + 1, y + 1]])

        meanArray = [mean1, mean2, mean3, mean4]
        dispersionArray = [dispersion1, dispersion2, dispersion3, dispersion4]
        pixelRGB = meanArray[(dispersionArray.index(min(dispersionArray)))]

        newimg.putpixel((x, y), (int(pixelRGB[0]), int(pixelRGB[1]), int(pixelRGB[2])))
       # pixelMap[x, y] = (int(pixelRGB), int(pixelRGB), int(pixelRGB))

#convertedImg.save("mostTone.bmp")
#convertedImg.show()
newimg.save("mostTone.bmp")
newimg.show()