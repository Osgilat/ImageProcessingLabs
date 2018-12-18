import csv
import itertools

import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt
from matplotlib import patches

img = Image.open("Row.bmp")
img = img.convert('1')

width = img.size[0]
height = img.size[1]

pixelMap = img.load()

maxVpr = 0
colList = []

for x in range(1, width, 1):
    colSum = 0
    for y in range(1, height, 1):
        if pixelMap[x, y] == 0:
            colSum += 1
    if colSum > maxVpr: maxVpr = colSum
    colList.append(colSum)

print('colList ' + str(colList))

maxHpr = 0
rowList = []

for y in range(1, height, 1):
    rowSum = 0
    for x in range(1, width, 1):
        if pixelMap[x, y] == 0:
            rowSum += 1
    if rowSum > maxHpr: maxHpr = rowSum
    rowList.append(rowSum)

colCoordsList = []

zeroSequence = False

for pos in range(1, len(colList), 1):
    if colList[pos] == 0:
        if not zeroSequence:
            colCoordsList.append(pos)
        zeroSequence = True
    else:
        if zeroSequence:
            colCoordsList.append(pos)
        zeroSequence = False

print(colCoordsList)

rowCoordsList = []

zeroSequence = False

for pos in range(1, len(rowList), 1):
    if rowList[pos] == 0:
        if not zeroSequence:
            rowCoordsList.append(pos)
        zeroSequence = True
    else:
        if zeroSequence:
            rowCoordsList.append(pos)
        zeroSequence = False

# Create figure and axes

fig, ax = plt.subplots(1)

# Display the image
ax.imshow(img)

symbolHorProfile = []

symbolNum = 0

with open('C:/stats2.csv', 'w') as file:
    for pos in range(0, len(colCoordsList) - 1, 1):

        if pos == 0:
            rect = patches.Rectangle((0, 0), colCoordsList[pos], height, linewidth=1, edgecolor='g', facecolor='none')
            symbolHorProfile = colList[0:colCoordsList[pos]]
            crop_rectangle = (0, 0, colCoordsList[pos], height)
            cropped_im = img.crop(crop_rectangle)
        elif pos == len(colCoordsList):
            rect = patches.Rectangle((colCoordsList[pos - 1], 0), colCoordsList[pos], height, linewidth=1,
                                     edgecolor='g',
                                     facecolor='none')
            symbolHorProfile = colList[colCoordsList[pos - 1]:colCoordsList[pos]]
            crop_rectangle = (colCoordsList[pos - 1], 0, colCoordsList[pos], height)
            cropped_im = img.crop(crop_rectangle)
        else:
            rect = patches.Rectangle((colCoordsList[pos], 0), colCoordsList[pos + 1] - colCoordsList[pos], height,
                                     linewidth=1, edgecolor='g', facecolor='none')
            symbolHorProfile = colList[colCoordsList[pos]:colCoordsList[pos + 1]]
            crop_rectangle = (colCoordsList[pos], 0, colCoordsList[pos + 1], height)
            cropped_im = img.crop(crop_rectangle)

        if pos % 2 != 0 or pos == 0:
            print('Symbol hor profile ' + str(symbolNum) + ' ' + str(symbolHorProfile))

            symbolPixelMap = cropped_im.load()

            width = cropped_im.size[0]
            height = cropped_im.size[1]

            blackSum = 0
            xsum = 0
            ysum = 0

            for x in range(1, width, 1):
                for y in range(1, height, 1):
                    if symbolPixelMap[x, y] == 0:
                        blackSum += 1
                        xsum += x
                        ysum += y

            comX = xsum / blackSum
            comY = ysum / blackSum

            iX = 0
            iY = 0

            for x in range(1, width, 1):
                for y in range(1, height, 1):
                    if pixelMap[x, y] == 0:
                        iX += (y - comY) ** 2
                        iY += (x - comX) ** 2

            blackSumByArea = blackSum / (width * height)

            nComX = round(comX / width, 2)
            nComY = round(comY / height, 2)

            niX = round(iX, 2) / (width ** 2 + height ** 2)
            niY = round(iY, 2) / (width ** 2 + height ** 2)

            file.write(
                str(str(symbolNum)) + ','
                + str(blackSum) + ','
                + str(blackSumByArea) + ','
                + str(comX) + ','
                + str(comY) + ','
                + str(round(comX / width, 2)) + ','
                + str(round(comY / height, 2)) + ','
                + str(iX) + ','
                + str(iY) + ','
                + str(round(iX, 2) / (width ** 2 + height ** 2)) + ','
                + str(round(iY, 2) / (width ** 2 + height ** 2)) + ',' + '\n')

            symbolNum += 1

        ax.add_patch(rect)

with open("C:/stats.csv") as textfile1, open("C:/stats2.csv") as textfile2, open("C:/result.csv", 'w') as resultCSV:
    csv_reader1 = csv.reader(textfile1, delimiter=',')
    csv_reader2 = csv.reader(textfile2, delimiter=',')
    line_count = 0
    euclidString = ""

    for row1 in csv_reader1:
        blackSumByAreaFromFile1 = float(row1[2])

        nComXFromFile1 = float(row1[5])
        nComYFromFile1 = float(row1[6])
        niXFromFile1 = float(row1[9])
        niYFromFile1 = float(row1[10])

        for row2 in csv_reader2:
            blackSumByAreaFromFile2 = float(row2[2])
            nComXFromFile2 = float(row2[5])
            nComYFromFile2 = float(row2[6])
            niXFromFile2 = float(row2[9])
            niYFromFile2 = float(row2[10])

            euclidDistance = round((math.sqrt((blackSumByAreaFromFile2 - blackSumByAreaFromFile1) ** 2)
                                    + math.sqrt((nComXFromFile2 - nComXFromFile1) ** 2)
                                    + math.sqrt((nComYFromFile2 - nComYFromFile1) ** 2)

                                   #+ math.sqrt((niXFromFile2 - niXFromFile1) ** 2)
                                    #+ math.sqrt((niYFromFile2 - niYFromFile1) ** 2)
                                    )
                                   , 2)

            euclidString += ("(" + str(row2[0]) + ";" + str(euclidDistance) + ")" + ",")

        print(str(row1[0]) + "," + euclidString)
        textfile2.seek(0)
        resultCSV.write(str(row1[0]) + "," + euclidString + '\n')
        euclidString = ""
        line_count += 1


'''
with open('C:/stats.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:

        if line_count == symbolNum:
            blackSumByAreaFromFile = row[2]

            nComXFromFile = row[5]
            nComYFromFile = row[6]
            niXFromFile = row[9]
            niYFromFile = row[10]

            line_count += 1
        else:
            line_count += 1
'''
plt.show()
