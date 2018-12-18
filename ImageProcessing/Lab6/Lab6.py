from PIL import Image, ImageFont, ImageDraw
import math
import operator

#Compute all needed metrics(blackSum, xCoM, yCoM, xIM, yIM)
def ComputeImgMetrics(img):

    blackSum = 0
    xCom = 0
    yCom = 0
    xIM = 0
    yIM = 0

    #Compute black pixels sum and image center of masses
    for x in range(img.size[0] - 1):
        for y in range(img.size[1] - 1):
            if img.getpixel((x, y)) < 1:
                blackSum += 1
                xCom += x
                yCom += y

    xCom = int(xCom / blackSum)
    yCom = int(yCom / blackSum)

    #Get image's image moments density and normalize metrics
    for x in range(img.size[0] - 1):
        for y in range(img.size[1] - 1):
            if img.getpixel((x, y)) < 1:
                xIM += math.pow(y - yCom, 2)
                yIM += math.pow(x - xCom, 2)

    density = blackSum / (img.size[0] * img.size[1])

    com = (xCom, yCom)

    relCom = (round((com[0] - 1) / (img.size[0] - 1), 2), round((com[1] - 1) / (img.size[1] - 1), 2))

    relxIM = round(xIM / (img.size[0] * img.size[0] + img.size[1] * img.size[1]), 2)
    relyIM = round(yIM / (img.size[0] * img.size[0] + img.size[1] * img.size[1]), 2)

    return (density, relCom[0], relCom[1], relxIM, relyIM)


def getXprofile(img):
    projX = [0] * img.size[0]
    for x in range(0, img.size[0]):
        projXY = 0
        for y in range(0, img.size[1]):
            projXY += (255 - img.getpixel((x, y)))
        projX[x] = projXY
    return projX


def getYprofile(img):
    projY = [0] * img.size[1]
    for y in range(0, img.size[1]):
        projYX = 0
        for x in range(0, img.size[0]):
            projYX += (255 - img.getpixel((x, y)))
        projY[y] = projYX
    return projY


def getSimilarity(charMetrics, charProfile, standardMetrics, standardProfile):
    result = 0
    for i in range(0, 3):
        result += math.pow(charMetrics[i] - standardMetrics[i], 2)
    profileRange = 0
    for i in range(0, 50):
        profileRange += abs(charProfile[0][i] - standardProfile[0][i])
        profileRange += abs(charProfile[1][i] - standardProfile[1][i])
    profileRange = round(profileRange / 100 / 12750, 2)
    result += math.pow(profileRange, 2)
    result = 1 - math.sqrt(result)
    return result


def getExtremePoints(proj):
    x1 = 0
    x2 = 0
    isWaitingForSymbol = True
    for x in range(0, len(proj)):
        if proj[x] < 125:
            if isWaitingForSymbol:
                continue
            x2 = x
            break
        else:
            if isWaitingForSymbol:
                x1 = x
                isWaitingForSymbol = False
    return (x1, x2)


def cutChar(img):
    projX = getXprofile(img)
    projY = getYprofile(img)
    x = getExtremePoints(projX)
    y = getExtremePoints(projY)
    return img.crop((x[0], y[0], x[1], y[1]))


alphabetMetricsData = {}
alphabetProfiles = {}
font = ImageFont.truetype("times_new_roman.ttf", 52)

#Generate images collection to compare row against
for char in "0123456789":
    img = Image.new("RGB", (50, 50), "white")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=(0, 0, 0))
    img = cutChar(img.convert("L"))
    img = img.resize((50, 50))
    img.save("alphabet/" + char + ".bmp")
    #Also save each number metrics and profile
    alphabetMetricsData[char] = ComputeImgMetrics(img)
    alphabetProfiles[char] = (getXprofile(img), getYprofile(img))

#Open image to cut it for numbers
img = Image.open("numbers.bmp")
img = img.convert("L")
width = img.size[0]
height = img.size[1]
projX = getXprofile(img)
points = [(0, 0, 0, 0) for i in range(10)]
isWaitingForSymbol = True
i = 0
leftPoint = 0
for x in range(0, width):
    if projX[x] < 125:
        if isWaitingForSymbol:
            continue
        isWaitingForSymbol = True
        points[i] = (leftPoint, 0, x, height)
        i += 1
    else:
        if isWaitingForSymbol:
            leftPoint = x
            isWaitingForSymbol = False

#Write to csv all metrics and sort number hypothesis by likelyhood
f = open("result.csv", "w+")
for i in range(0, len(points)):
    charImg = img.crop(points[i]).resize((50, 50))
    charMetrics = ComputeImgMetrics(charImg)
    similarity = {}
    for char in "0123456789":
        similarity[char] = getSimilarity(charMetrics, (getXprofile(charImg), getYprofile(charImg)),
                                         alphabetMetricsData[char], alphabetProfiles[char])
    sortedSimilarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    f.write(str(i + 1) + ": [")
    for item in sortedSimilarity:
        f.write("(\"" + item[0] + "\", " + str(item[1]) + "),")
    f.write("]" + "\n")
f.close()