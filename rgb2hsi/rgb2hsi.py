from PIL import Image, ImageOps
import numpy as np

imgFile = input('Digite o nome da imagem: ')
imgName = imgFile.split('.')[0]

imgRgb = Image.open(f'rgb-images/{imgFile}', 'r')
imgRgb = ImageOps.exif_transpose(imgRgb)

arrayRgb = np.asarray(imgRgb)

arrayHsi = np.zeros((imgRgb.height, imgRgb.width, 3), dtype = np.uint8)
arrayH = np.zeros((imgRgb.height, imgRgb.width), dtype = np.uint8)
arrayS = np.zeros((imgRgb.height, imgRgb.width), dtype = np.uint8)
arrayI = np.zeros((imgRgb.height, imgRgb.width), dtype = np.uint8)

i = 0
j = 0
for pixelLine in arrayRgb:
    for pixel in pixelLine:
        r = float(pixel[0]) / 255
        g = float(pixel[1]) / 255
        b = float(pixel[2]) / 255

        numerador = ((r - g) + (r - b)) / 2
        denominador = ((r - g) ** 2 + (r - b) * (g - b)) ** 0.5

        teta = np.degrees(np.arccos(numerador / (denominador + 0.00001)))

        if b < g:
            hue = teta
        else:
            hue = 360 - teta

        divSat = 0
        if r + g + b == 0:
            divSat = 1
        else:
            divSat = 3 / (r + g + b)

        sat = 1 - divSat * min(r, g, b)

        inten = (r + g + b) / 3

        arrayHsi[i][j][0] = (hue / 360) * 255
        arrayHsi[i][j][1] = sat * 255
        arrayHsi[i][j][2] = inten * 255

        arrayH[i][j] = (hue / 360) * 255
        arrayS[i][j] = sat * 255
        arrayI[i][j] = inten * 255

        j += 1
    
    j = 0
    i += 1

imgH = Image.fromarray(arrayH, mode='L')
imgH.show()

imgS = Image.fromarray(arrayS, mode='L')
imgS.show()

imgI = Image.fromarray(arrayI, mode='L')
imgI.show()

imgHsv = Image.fromarray(arrayHsi, mode='HSV')
imgHsv.show()
