import numpy as np
from PIL import Image, ImageOps

L = 256

imgFile = input('Digite o nome da imagem: ')
imgName = imgFile.split('.')[0]

img = Image.open(f'images/{imgFile}')
img = ImageOps.exif_transpose(img)
img = ImageOps.grayscale(img)

totalPixels = img.height * img.width

imgArray = np.asarray(img)

histogram = np.zeros(256)

# Histograma
for pixelLine in imgArray:
    for pixel in pixelLine:
        histogram[pixel] += 1

# Histograma Normalizado
normalHist = np.zeros(256)

for value in range(len(histogram)):
    normalHist[value] = histogram[value] / totalPixels

# Média Global
mg = 0
for i in range(L):
    mg += i * normalHist[i]

variance = []
for t in range(1, L):
    p1 = 0
    p1Aux = 0

    teste = 0
    for i in range(t):
        p1 += normalHist[i]

        p1Aux += i * normalHist[i]
    
    p2 = 1 - p1

    if(p1 != 0):
        m1 = (1 / p1) * p1Aux
    else:
        m1 = p1Aux

    p2Aux = 0
    for i in range(t + 1, L):
        p2Aux += i * normalHist[i]

    if p2 != 0:
        m2 = (1 / p2) * p2Aux
    else:
        m2 = p2Aux

    variance.append(p1 * (m1 - mg) ** 2 + p2 * (m2 - mg) ** 2)

maxVariance = max(variance)
threshold = variance.index(maxVariance)

segmentedImgArray = np.zeros((img.height, img.width), dtype=np.uint8)
for x in range(img.height):
    for y in range(img.width):
        if imgArray[x, y] <= threshold:
            segmentedImgArray[x, y] = 0
        else:
            segmentedImgArray[x, y] = 255

segmentedImg = Image.fromarray(segmentedImgArray, mode='L').convert('1')
segmentedImg.save(f'segmented-images/{imgName}.jpg', format='JPEG')
