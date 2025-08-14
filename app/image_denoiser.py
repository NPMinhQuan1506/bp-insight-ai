import math


def aid_applyGaussianBlur(grayScale_Matrix, kernelSize=3, sigma=1.0):
    if not grayScale_Matrix or not grayScale_Matrix[0]:
        return []

    if kernelSize % 2 == 0:
        raise ValueError("The size of kernel must be an odd number")

    kernel = []
    kernelSum = 0.0
    radius = kernelSize // 2
    print("Formula: G(x,y) = (1/(2πσ²)) * e^(-(x²+y²)/(2σ²))")
    for i in range(-radius, radius + 1):
        row = []
        for j in range(-radius, radius + 1):
            exponentNumerator = -(i**2 + j**2)
            exponentDenominator = 2 * sigma**2

            weight = math.exp(exponentNumerator / exponentDenominator)
            row.append(weight)
            kernelSum += weight

        kernel.append(row)

    for i in range(kernelSize):
        for j in range(kernelSize):
            kernel[i][j] /= kernelSum

    height = len(grayScale_Matrix)
    width = len(grayScale_Matrix[0])

    blurredMatrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):

            weightedSum = 0.0

            for ky in range(-radius, radius + 1):
                for kx in range(-radius, radius + 1):
                    neighborVert = y + ky
                    neighborHor = x + kx

                    if 0 <= neighborVert < height and 0 <= neighborHor < width:
                        pixelValue = grayScale_Matrix[neighborVert][neighborHor]
                        weight = kernel[ky + radius][kx + radius]
                        weightedSum += pixelValue * weight

            blurredMatrix[y][x] = int(round(weightedSum))

    return blurredMatrix
