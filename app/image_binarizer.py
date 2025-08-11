from __future__ import annotations


def aib_binarized(grayScale_Matrix, threshold=128):
    if not grayScale_Matrix:
        return []

    height = len(grayScale_Matrix)
    width = len(grayScale_Matrix[0])

    binary = []
    for y in range(height):
        row = []
        for x in range(width):
            px = grayScale_Matrix[y][x]
            row.append(1 if px >= threshold else 0)
        binary.append(row)

    return binary


def aib_binarized_otsu(grayScale_Matrix):
    if not grayScale_Matrix:
        return []

    hist = [0] * 256
    total = 0
    for row in grayScale_Matrix:
        for px in row:
            hist[px] += 1
            total += 1

    sumTotal = sum(i * hist[i] for i in range(256))
    sum_b = 0
    w_b = 0
    maxVar = -1.0
    best_t = 0

    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break

        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sumTotal - sum_b) / w_f
        varBetween = w_b * w_f * (m_b - m_f) ** 2
        if varBetween > maxVar:
            maxVar = varBetween
            best_t = t
    return aib_binarized(grayScale_Matrix, threshold=best_t)
