from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

imgFile = input('Digite o nome da imagem: ')
imgName = imgFile.split('.')[0]

img = Image.open(f'images/{imgFile}')
img = ImageOps.exif_transpose(img)

totalPixels = img.width * img.height

imgArray = np.asarray(img)

if(imgArray[0][0].size > 1):
    grayscale = False

    print('\033[4;31mAtenção!!')
    print('\033[0;34mEqualizar imagens coloridas (como imagens RGB) pode alterar significativamente o equilíbrio das cores.\033[;;m')
else:
    grayscale = True

if grayscale:
    histogram = np.zeros(256)
else:
    histogram = np.zeros((3, 256))

# Histograma
for pixelLine in imgArray:
    for pixel in pixelLine:
        if grayscale:
            histogram[pixel] += 1
        else:
            histogram[0, pixel[0]] += 1
            histogram[1, pixel[1]] += 1
            histogram[2, pixel[2]] += 1

if grayscale:
    plt.plot(histogram, color='gray')
    
    plt.title('Grayscale Histogram')
    plt.xlabel('Value')
else:
    plt.plot(histogram[0], color='red')
    plt.plot(histogram[1], color='green')
    plt.plot(histogram[2], color='blue')

    plt.title('Color Histogram')
    plt.xlabel('Color Value')

plt.ylabel('Frequency')

plt.show()

# Histograma Normalizado
if grayscale:
    normalHist = np.zeros(256)

    for value in range(len(histogram)):
        normalHist[value] = histogram[value] / totalPixels

    plt.plot(normalHist, color='gray')

    plt.title('Normalized Grayscale Histogram')
    plt.xlabel('Value')
else:
    normalHist = np.zeros((3, 256))

    for color in range(len(histogram)):
        for value in range(len(histogram[color])):
            normalHist[color, value] = histogram[color, value] / totalPixels

    plt.plot(normalHist[0], color='red')
    plt.plot(normalHist[1], color='green')
    plt.plot(normalHist[2], color='blue')

    plt.title('Normalized Color Histogram')
    plt.xlabel('Color Value')

plt.ylabel('Frequency')

plt.show()

# Histograma Acumulado
if grayscale:
    accumulatedHistogram = np.zeros(256)

    for value in range(len(normalHist)):
        if value != 0:
            accumulatedHistogram[value] = accumulatedHistogram[value - 1] + normalHist[value]
        else:
            accumulatedHistogram[value] = normalHist[value]

    plt.plot(accumulatedHistogram, color='gray')

    plt.title('Accumulated Grayscale Histogram')
    plt.xlabel('Value')
else:
    accumulatedHistogram = np.zeros((3, 256))

    for color in range(len(normalHist)):
        for frequency in range(len(histogram[color] - 1)):
            if frequency != 0:
                accumulatedHistogram[color, frequency] = accumulatedHistogram[color, frequency - 1] + normalHist[color, frequency]
            else:
                accumulatedHistogram[color, frequency] = normalHist[color, frequency]

    plt.plot(accumulatedHistogram[0], color='red')
    plt.plot(accumulatedHistogram[1], color='green')
    plt.plot(accumulatedHistogram[2], color='blue')

    plt.title('Accumulated Color Histogram')
    plt.xlabel('Color Value')

plt.ylabel('Frequency')

plt.show()

# Imagem equalizada
if grayscale:
    equalizedArray = np.zeros((img.height, img.width), dtype=np.uint8)
else:
    equalizedArray = np.zeros((img.height, img.width, 3), dtype=np.uint8)

for i in range(img.height):
    for j in range(img.width):
        if grayscale:
            equalizedArray[i, j] = round(255 * accumulatedHistogram[imgArray[i, j]])
        else:
            for k in range(3):
                equalizedArray[i, j, k] = round(255 * accumulatedHistogram[k, imgArray[i, j, k]])

if grayscale:
    equalizedImg = Image.fromarray(equalizedArray, mode='L')
else:
    equalizedImg = Image.fromarray(equalizedArray, mode='RGB')
equalizedImg.save(f'equalized-images/{imgName}.jpg', format='JPEG')
equalizedImg.show()

# Histograma Após Equalização
for pixelLine in equalizedArray:
    for pixel in pixelLine:
        if grayscale:
            histogram[pixel] += 1
        else:
            histogram[0, pixel[0]] += 1
            histogram[1, pixel[1]] += 1
            histogram[2, pixel[2]] += 1

if grayscale:
    plt.plot(histogram, color='gray')
    
    plt.title('Grayscale Histogram')
    plt.xlabel('Value')
else:
    plt.plot(histogram[0], color='red')
    plt.plot(histogram[1], color='green')
    plt.plot(histogram[2], color='blue')

    plt.title('Color Histogram')
    plt.xlabel('Color Value')

plt.ylabel('Frequency')

plt.show()
