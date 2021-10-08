from PIL import Image, ImageOps
import numpy as np

imgFile = input('Digite o nome da imagem: ')
imgName = imgFile.split('.')[0]

imgRgb = Image.open(f'rgb-images/{imgFile}')
imgRgb = ImageOps.exif_transpose(imgRgb)

arrayRgb = np.asarray(imgRgb)

arrayCmyk = np.zeros((imgRgb.height, imgRgb.width, 4), dtype = np.uint8)
arrayC = np.zeros((imgRgb.height, imgRgb.width, 4), dtype = np.uint8)
arrayM = np.zeros((imgRgb.height, imgRgb.width, 4), dtype = np.uint8)
arrayY = np.zeros((imgRgb.height, imgRgb.width, 4), dtype = np.uint8)
arrayK = np.zeros((imgRgb.height, imgRgb.width, 4), dtype = np.uint8)

i = 0
j = 0
for pixelLine in arrayRgb:
    for pixel in pixelLine:
        rPrime = pixel[0] / 255
        gPrime = pixel[1] / 255
        bPrime = pixel[2] / 255

        k = 1 - max(rPrime, gPrime, bPrime)

        if k != 1:
            c = (1 - rPrime - k) / (1 - k)
            m = (1 - gPrime - k) / (1 - k)
            y = (1 - bPrime - k) / (1 - k)
        else:
            c = 0
            m = 0
            y = 0

        # Imagem completa (4 camadas)
        arrayCmyk[i][j][0] = c * 255
        arrayCmyk[i][j][1] = m * 255
        arrayCmyk[i][j][2] = y * 255
        arrayCmyk[i][j][3] = k * 255

        # Camadas Separadas
        arrayC[i][j][0] = c * 255
        arrayM[i][j][1] = m * 255
        arrayY[i][j][2] = y * 255
        arrayK[i][j][3] = k * 255

        j += 1
    
    j = 0
    i += 1

imgC = Image.fromarray(arrayC, mode='CMYK')
imgC.save(f'cmyk-images/{imgName}_C.jpg', format='JPEG')

imgM = Image.fromarray(arrayM, mode='CMYK')
imgM.save(f'cmyk-images/{imgName}_M.jpg', format='JPEG')

imgY = Image.fromarray(arrayY, mode='CMYK')
imgY.save(f'cmyk-images/{imgName}_Y.jpg', format='JPEG')

imgK = Image.fromarray(arrayK, mode='CMYK')
imgK.save(f'cmyk-images/{imgName}_K.jpg', format='JPEG')

imgCmyk = Image.fromarray(arrayCmyk, mode='CMYK')
imgCmyk.save(f'cmyk-images/{imgName}.jpg', format='JPEG')
