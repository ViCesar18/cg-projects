from PIL import Image, ImageOps
import numpy as np

import frequency_filters

def calculateAlpha(u, n):
    if u == 0:
        return np.sqrt(1 / n)
    else:
        return np.sqrt(2 / n)


def calculateCalcCosine(x, u, n):
    calc = (2 * x + 1) * u * np.pi / (2 * n)

    return np.cos(calc)


def calculateDiscreteCosineTransform(matrix, n, m):
    frequencyArray = np.zeros((n, m), dtype=np.double)

    for u in range(n):
        for v in range(m):
            sum = 0

            for x in range(n):
                for y in range(m):
                    sum += matrix[x, y] * calculateCalcCosine(x, u, n) * calculateCalcCosine(y, v, m)
            
            frequencyArray[u, v] = calculateAlpha(u, n) * calculateAlpha(v, m) * sum

    return frequencyArray


def calculateInverseDiscreteCosineTransform(matrix, n, m):
    array = np.zeros((n, m), dtype=np.double)

    for x in range(n):
        for y in range(m):
            sum = 0

            for u in range(n):
                for v in range(m):
                    sum += calculateAlpha(u, n) * calculateAlpha(v, m) * matrix[u, v] * calculateCalcCosine(x, u, n) * calculateCalcCosine(y, v, m)
            
            array[x, y] = sum
    
    return array


def transformArrayToGrayscale(matrix, n, m):
    grayscale = np.zeros((n, m), dtype=np.uint8)

    for i in range(n):
        for j in range(m):
            if matrix[i, j] <= 0:
                grayscale[i, j] = 0
            elif matrix[i, j] >= 255:
                grayscale[i, j] = 255   
            else:
                grayscale[i, j] = matrix[i, j]

    return grayscale


def pointIsInsideRect(x, y, w, h, px, py):
    if px >= x and px <= x + w and py >= y and py <= y + h:
        return True

    return False

def generateNoise(frequencyArray, n, m):
    noisedImage = np.zeros((n, m), dtype=np.double)

    for x in range(n):
        for y in range(m):
            if pointIsInsideRect(n / 2, m / 2, 5, 5, x, y):
                noisedImage[x, y] = 255
            else:
                noisedImage[x, y] = frequencyArray[x, y]

    return noisedImage


imgFile = input('Digite o nome da imagem: ')
imgName = imgFile.split('.')[0]

lowPassR = int(input('Digite o raio do corte para o Filtro Passa-Baixa: '))
highPassR = int(input('Digite o raio do corte para o Filtro Passa-Alta: '))

img = Image.open(f'images/{imgFile}')
img = ImageOps.exif_transpose(img)

imgArray = np.asarray(img)

# Frequência
print('\nCalculando a frequência da imagem através da Transformada Discreta do Cosseno...\n')
frequencyArray = calculateDiscreteCosineTransform(imgArray, img.height, img.width)
grayscaleFrequencyArray = transformArrayToGrayscale(frequencyArray, img.height, img.width)

frequencyImg = Image.fromarray(grayscaleFrequencyArray, mode='L')
frequencyImg.save(f'frequency-images/{imgName}.png', format='PNG')

# Frequencia Inversa
print('Gerando a imagem original através da Transformada Inversa Discreta do Cosseno...\n')
inverseArray = calculateInverseDiscreteCosineTransform(frequencyArray, img.height, img.width)
grayscaleInverseArray = transformArrayToGrayscale(inverseArray, img.height, img.width)

inverseImg = Image.fromarray(grayscaleInverseArray, mode='L')
inverseImg.save(f'inverse-images/{imgName}.png', format='PNG')

# Passa-Baixa
print('Aplicando o filtro Passa-Baixa na frequência...\n')
lowPassFreqArray = frequency_filters.idealLowPassFilter(frequencyArray, lowPassR, img.height, img.width)
grayscaleLowPassFreqArray = transformArrayToGrayscale(lowPassFreqArray, img.height, img.width)

lowPassFreqImg = Image.fromarray(grayscaleLowPassFreqArray, mode='L')
lowPassFreqImg.save(f'low-pass-filter-images/{imgName}-frequency-{lowPassR}.png', format='PNG')

# Passa-Baixa (Inversa)
print('Gerando a imagem original com o filtro Passa-Baixa aplicado através da Transformada Inversa Discreta do Cosseno...\n')
lowPassImgArray = calculateInverseDiscreteCosineTransform(lowPassFreqArray, img.height, img.width)
grayscaleLowPassImgArray = transformArrayToGrayscale(lowPassImgArray, img.height, img.width)

lowPassImg = Image.fromarray(grayscaleLowPassImgArray, mode='L')
lowPassImg.save(f'low-pass-filter-images/{imgName}-{lowPassR}.png', format='PNG')

# Passa-Alta
print('Aplicando o filtro Passa-Alta na frequência...\n')
highPassFreqArray = frequency_filters.idealHighPassFilter(frequencyArray, highPassR, img.height, img.width)
grayscaleHighPassFreqArray = transformArrayToGrayscale(highPassFreqArray, img.height, img.width)

highPassFreqImg = Image.fromarray(grayscaleHighPassFreqArray, mode='L')
highPassFreqImg.save(f'high-pass-filter-images/{imgName}-frequency-{highPassR}.png', format='PNG')

# Passa-Alta (Inversa)
print('Gerando a imagem original com o filtro Passa-Alta aplicado através da Transformada Inversa Discreta do Cosseno...\n')
highPassImgArray = calculateInverseDiscreteCosineTransform(highPassFreqArray, img.height, img.width)
grayscaleHighPassImgArray = transformArrayToGrayscale(highPassImgArray, img.height, img.width)

highPassImg = Image.fromarray(grayscaleHighPassImgArray, mode='L')
highPassImg.save(f'high-pass-filter-images/{imgName}-{highPassR}.png', format='PNG')

# Geração de ruído na frequência
print('Gerando ruído na frequência da imagem...\n')
noisedFrequencyArray = generateNoise(frequencyArray, img.height, img.width)
grayscaleNoisedFreqArray = transformArrayToGrayscale(noisedFrequencyArray, img.height, img.width)

noisedFrequencyImg = Image.fromarray(grayscaleNoisedFreqArray, mode='L')
noisedFrequencyImg.save(f'noised-images/{imgName}-frequency.png', format='PNG')

# Geração da imagem com frequência ruidosa
print('Gerando a nova imagem a partir da frequência ruidosa...\n')
noisedImgArray = calculateInverseDiscreteCosineTransform(noisedFrequencyArray, img.height, img.width)
grayscaleNoisedImgArray = transformArrayToGrayscale(noisedImgArray, img.height, img.width)

noisedImg = Image.fromarray(grayscaleNoisedImgArray, mode='L')
noisedImg.save(f'noised-images/{imgName}.png')
