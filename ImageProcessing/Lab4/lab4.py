import os

from PIL import Image, ImageFont, ImageDraw
import numpy
from numpy import mgrid, sum


font = ImageFont.truetype("arial.ttf", 52)


for char in "1234567890":
	img = Image.new('RGB', (50, 50), "white")
	img = img.convert('1')
	draw = ImageDraw.Draw(img)
	draw.text((0, 0), char, "black", font=font)
	img.save("C:/alphabet/"+char+".jpg", "JPEG")



'''
for image in os.listdir("C:/alphabet/"):
	print(image)
'''




with open('C:/stats.csv','w') as file:
	for image in os.listdir("C:/alphabet/"):
		imag = Image.open("C:/alphabet/"+image)

		pixelMap = imag.load()
		blackSum = 0
		xsum = 0
		ysum = 0

		for x in range(1, 50, 1):
			for y in range(1, 50, 1):
				if pixelMap[x, y] == 0:
					blackSum += 1
					xsum += x
					ysum += y

		comX = xsum / blackSum
		comY = ysum / blackSum

		iX = 0
		iY = 0

		for x in range(1, 50, 1):
			for y in range(1, 50, 1):
				if pixelMap[x, y] == 0:
					iX += (y - comY) ** 2
					iY += (x - comX) ** 2

		'''
		img = numpy.array(imag)
		blackSum = numpy.sum(img == 0)
		'''
		blackSumByArea = blackSum / (50 * 50)

		file.write(
			str("C:/alphabet/"+image) + ','
			+ str(blackSum) + ','
			+ str(blackSumByArea) + ','
				   + str(comX)  + ','
				   + str(comY) + ','
				   + str(round(comX / 50, 2)) + ','
				   + str(round(comY / 50, 2))   + ','
				   + str(iX) + ','
				   + str(iY) + ','
				   + str(round(iX, 2) / (50**2 + 50**2)) + ','
				   + str(round(iY, 2) / (50**2 + 50**2)) + ',' + '\n')
