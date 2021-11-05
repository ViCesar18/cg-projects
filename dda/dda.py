def dda(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    x = x1
    y = y1

    print('\nPontos que devem ser pintados:')
    while x <= x2:
        print(f'({round(x, 2)}, {round(y, 2)})')

        x += 1
        y += m


x1 = float(input('Forneça o valor de X1: '))
y1 = float(input('Forneça o valor de Y1: '))

x2 = float(input('Forneça o valor de X2: '))
y2 = float(input('Forneça o valor de Y2: '))

dda(x1, y1, x2, y2)
