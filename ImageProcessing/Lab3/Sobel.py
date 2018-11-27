from PIL import Image
import math

img = Image.open("original-flower.jpg")

width = img.size[0]
height = img.size[1]

maxG = 0

tempimg = Image.new("RGB", (width, height), "white")
finalimg = Image.new("RGB", (width, height), "white")
for x in range(1, width-1):
    for y in range(1, height-1):

        Gx = 0
        Gy = 0

        p = img.getpixel((x-1, y-1))
        r = p[0]
        g = p[1]
        b = p[2]

        intensity = r + g + b

        """
        SOBEL MASK
        Gy
        -1 -2 -1 
         0  0  0
         1  2  1
        Gx       
        -1  0  1 
        -2  0  2
        -1  0  1
         """

        Gx += -intensity
        Gy += -intensity

        p = img.getpixel((x-1, y))
        r = p[0]
        g = p[1]
        b = p[2]

        Gx += -2 * (r + g + b)

        p = img.getpixel((x-1, y+1))
        r = p[0]
        g = p[1]
        b = p[2]

        Gx += -(r + g + b)
        Gy += (r + g + b)

        p = img.getpixel((x, y-1))
        r = p[0]
        g = p[1]
        b = p[2]

        Gy += -2 * (r + g + b)

        p = img.getpixel((x, y+1))
        r = p[0]
        g = p[1]
        b = p[2]

        Gy += 2 * (r + g + b)

        p = img.getpixel((x+1, y-1))
        r = p[0]
        g = p[1]
        b = p[2]

        Gx += (r + g + b)
        Gy += -(r + g + b)

        p = img.getpixel((x+1, y))
        r = p[0]
        g = p[1]
        b = p[2]

        Gx += 2 * (r + g + b)

        p = img.getpixel((x+1, y+1))
        r = p[0]
        g = p[1]
        b = p[2]

        Gx += (r + g + b)
        Gy += (r + g + b)

        length = math.sqrt((Gx * Gx) + (Gy * Gy))

        length = max(0, min((255, int(length))))

        if length > maxG:
            maxG = length

        tempimg.putpixel((x, y), (length, length, length))

for x in range(1, width-1):
    for y in range(1, height-1):
        normalizedG = (tempimg.getpixel((x, y))[0] / maxG) * 255
        normalizedG = int(normalizedG)
        if normalizedG > 250:
            normalizedG = 255

        else:
            normalizedG = 0
        finalimg.putpixel((x, y), (normalizedG, normalizedG, normalizedG))

finalimg.save("tempFlower2.bmp")
finalimg.show()