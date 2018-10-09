from PIL import Image

img = Image.open("forest.bmp")

width = img.size[0]
height = img.size[1]

heightToChangeTo = 400

print("Original width " + str(width))
print("Original height " + str(height))
'''
changedWidth = width / 2
changedHeight = height / 5

newimg = img.resize((int(changedWidth), int(changedHeight)), Image.ANTIALIAS)

newimg.save("resized_image.jpg")
'''


heightPercent = (heightToChangeTo / height)
adaptableWidth = int((float(width) * float(heightPercent)))
newimg = img.resize((adaptableWidth, heightToChangeTo))

Image._show(newimg)