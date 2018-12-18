from PIL import Image
import math

img = Image.open("forest.bmp")
width = img.size[0]
height = img.size[1]

adjacencyMatrix = [[float(0)] * 256 for i in range(256)]
adjacencyNumber = (width) * (height)
for x in range(1, width - 1):
    for y in range(1, height - 1):
        p45 = int(sum(img.getpixel((x - 1, y - 1))) / 3)
        p135 = int(sum(img.getpixel((x + 1, y - 1))) / 3)
        p = int(sum(img.getpixel((x, y))) / 3)
        p225 = int(sum(img.getpixel((x + 1, y + 1))) / 3)
        p315 = int(sum(img.getpixel((x - 1, y + 1))) / 3)

        adjacencyMatrix[p][p45] += 1
        adjacencyMatrix[p][p135] += 1
        adjacencyMatrix[p][p225] += 1
        adjacencyMatrix[p][p315] += 1

f = open("result.csv", "w+")
f.write(";")
for i in range(1, 256):
    f.write(str(i) + ";")
f.write("\n")

mpr = float(0)

mpr = max(max(x) for x in adjacencyMatrix)

adjacencyImg = Image.new('RGB', (255, 255))
pixels = adjacencyImg.load()
for x in range(0, 255):
    f.write(str(x + 1) + ";")
    for y in range(0, 255):
        pixelBrightness = int(255 * adjacencyMatrix[x][y] / mpr)
        pixels[x,y] = (pixelBrightness,pixelBrightness,pixelBrightness)
        f.write(str(adjacencyMatrix[x][y]) + ";")
    f.write("\n")
adjacencyImg.show()
adjacencyImg.save("charalic.bmp")

f.write("\n")
f.write("MPR;" + str(mpr) + "\n")
f.close()