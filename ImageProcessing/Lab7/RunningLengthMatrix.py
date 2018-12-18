from PIL import Image, ImageDraw
import math

img = Image.open("0.bmp")
width = img.size[0]
height = img.size[1]

glrlmMaxSize = max(width, height)
glrlm = [[0] * 256 for i in range(glrlmMaxSize)]

for i in range(2, width):
    # print(i)
    for y in range(0, height):
        x = 0
        while x < width:
            j = 1
            for z in range(1, i):
                if x + i > width:
                    break
                if int(sum(img.getpixel((x, y))) / 3) != int(sum(img.getpixel((x + z, y))) / 3):
                    break
                j = j + 1
            if j == i:
                if (x + j == width or int(sum(img.getpixel((x + j - 1, y))) / 3) != int(
                        sum(img.getpixel((x + j, y))) / 3)):
                    glrlm[i - 1][int(sum(img.getpixel((x, y))) / 4) - 1] += 1
                    x += i
                else:
                    while x + j < width and int(sum(img.getpixel((x + j - 1, y))) / 3) == int(
                            sum(img.getpixel((x + j, y))) / 3):
                        x += 1
                    x += 1
            else:
                x += 1

for i in range(2, height + 1):
    # print(i)
    for x in range(0, width):
        y = 0
        while y < height:
            j = 1
            for z in range(1, i):
                if y + i > height:
                    break
                if int(sum(img.getpixel((x, y))) / 3) != int(sum(img.getpixel((x, y + z))) / 3):
                    break
                j = j + 1
            if j == i:
                if (y + j == height or int(sum(img.getpixel((x, y + j - 1))) / 3) != int(
                        sum(img.getpixel((x, y + j))) / 3)):
                    glrlm[i - 1][int(sum(img.getpixel((x, y))) / 4) - 1] += 1
                    y += i
                else:
                    while y + j < height and int(sum(img.getpixel((x, y + j - 1))) / 3) == int(
                            sum(img.getpixel((x, y + j))) / 3):
                        y += 1
                    y += 1
            else:
                y += 1

f = open("glrlm.csv", "w+")
f.write(";")
for i in range(1, 256):
    f.write(str(i) + ";")
f.write("\n")

maxCount = 1
totalCount = 1
sre = 0
for x in range(0, glrlmMaxSize):
    f.write(str(x + 1) + ";")
    for y in range(0, 255):
        if glrlm[x][y] > maxCount:
            maxCount = glrlm[x][y]
        totalCount += glrlm[x][y]
        sre += glrlm[x][y] / math.pow(x + 1, 2)
        f.write(str(glrlm[x][y]) + ";")
    f.write("\n")
sre = sre / totalCount
f.write("\n")
f.write("\n")
f.write("SRE;" + str(sre) + "\n")
f.close()

glrlmImg = Image.new('RGB', (255, glrlmMaxSize))
pixels = glrlmImg.load()
for x in range(0, glrlmMaxSize):
    for y in range(0, 255):
        pixelBrightness = int(255 * glrlm[x][y] / maxCount)
        pixels[y, x] = (pixelBrightness, pixelBrightness, pixelBrightness)
glrlmImg.save("glrlm.jpg", "JPEG")

