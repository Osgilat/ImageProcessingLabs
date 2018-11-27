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

for pos in range(0, len(colCoordsList) - 1, 1):
    if pos == 0:
        rect = patches.Rectangle((0, 0), colCoordsList[pos], height, linewidth=1, edgecolor='g', facecolor='none')
        symbolHorProfile = colList[0:colCoordsList[pos]]
    elif pos == len(colCoordsList):
        rect = patches.Rectangle((colCoordsList[pos - 1], 0), colCoordsList[pos], height, linewidth=1, edgecolor='g',
                                 facecolor='none')
        symbolHorProfile = colList[colCoordsList[pos - 1]:colCoordsList[pos]]
    else:
        rect = patches.Rectangle((colCoordsList[pos], 0), colCoordsList[pos + 1] - colCoordsList[pos], height,
                                 linewidth=1, edgecolor='g', facecolor='none')
        symbolHorProfile = colList[colCoordsList[pos]:colCoordsList[pos + 1]]

    if pos % 2 != 0 or pos == 0:
        print('Symbol hor profile ' + str(symbolNum) + ' ' + str(symbolHorProfile))
        symbolNum += 1
    '''
    bins = np.linspace(math.ceil(min(symbolHorProfile)),
                       math.floor(max(symbolHorProfile)),
                       381)

    plt.xlim([min(symbolHorProfile) - 5, max(symbolHorProfile) + 5])

    plt.hist(symbolHorProfile, bins=bins, alpha=0.5)
    plt.title(str(pos) + ' Number')
    plt.xlabel('Horizontal profile')
    plt.ylabel('count')

    

    plt.show()
    '''

    ax.add_patch(rect)

    '''
    plt.hist(symbolHorProfile, bins=30, density=True, alpha=0.5,
             histtype='stepfilled', color='steelblue',
             edgecolor='none');
    plt.xlabel(str(pos))
    plt.show()
    '''

plt.show()
