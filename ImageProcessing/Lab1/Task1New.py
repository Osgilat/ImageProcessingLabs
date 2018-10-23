from PIL import Image

img = Image.open("forest.bmp")

width = img.size[0]
height = img.size[1]

widthFactor = 3
heightFactor = 1

newWidth = int(width*widthFactor)
newHeight = int(height*heightFactor)

newImage = Image.new("RGB", (newWidth, newHeight), "white")

for x in range(newWidth):
    for y in range(newHeight):
        p = img.getpixel((x / widthFactor, y / heightFactor))
        newImage.putpixel((x, y), p)

newImage.save("resized_image2.jpg")

newImage.show()

