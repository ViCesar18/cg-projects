import numpy as np

def getDist(x, y):
    return np.sqrt(x**2 + y**2)


def idealLowPassFilter(frequencyArray, r, n, m):
    newArray = np.zeros((n, m), dtype=np.double)

    for x in range(n):
        for y in range(m):
            dist = getDist(x, y)
            
            if dist <= r:
                newArray[x, y] = frequencyArray[x, y]
            else:
                newArray[x, y] = 0
    
    return newArray

def idealHighPassFilter(frequencyArray, r, n, m):
    newArray = np.zeros((n, m), dtype=np.double)

    for x in range(n):
        for y in range(m):
            dist = getDist(x, y)

            if dist > r:
                newArray[x, y] = frequencyArray[x, y]
            else:
                newArray[x, y] = 0
    
    return newArray
