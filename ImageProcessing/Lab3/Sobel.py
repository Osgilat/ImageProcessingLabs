from PIL import Image
import math

img = Image.open("original-flower.jpg")

width = img.size[0]
height = img.size[1]

newimg = Image.new("RGB", (width, height), "white")
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

        length = int(length)

        newimg.putpixel((x,y),(length,length,length))

newimg.save("sobel2.bmp")
newimg.show()