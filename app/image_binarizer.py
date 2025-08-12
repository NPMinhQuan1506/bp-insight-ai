from __future__ import annotations


def aib_binarizeWithFixedThreshold(grayscale_matrix, threshold=128):
    if not grayscale_matrix:
        return []

    rows = len(grayscale_matrix)
    cols = len(grayscale_matrix[0])

    binary_matrix = []
    for i in range(rows):
        new_row = []
        for j in range(cols):
            pixel = grayscale_matrix[i][j]
            binary_pixel = 1 if pixel >= threshold else 0
            new_row.append(binary_pixel)
        binary_matrix.append(new_row)

    return binary_matrix


def aib_binarizeWithOtsuThreshold(grayscale_matrix):
    if not grayscale_matrix:
        return []

    histogram = [0] * 256
    total_pixels = 0

    for row in grayscale_matrix:
        for pixel in row:
            histogram[pixel] += 1
            total_pixels += 1

    total_sum = 0
    for i in range(256):
        total_sum += i * histogram[i]

    bg_pixels = 0
    bg_sum = 0
    max_variance = -1.0
    best_threshold = 0

    for threshold in range(256):
        bg_pixels += histogram[threshold]
        bg_sum += threshold * histogram[threshold]

        if bg_pixels == 0:
            continue

        fg_pixels = total_pixels - bg_pixels

        if fg_pixels == 0:
            break

        bg_mean = bg_sum / bg_pixels
        fg_sum = total_sum - bg_sum
        fg_mean = fg_sum / fg_pixels

        variance = bg_pixels * fg_pixels * (bg_mean - fg_mean) ** 2

        if variance > max_variance:
            max_variance = variance
            best_threshold = threshold

    return aib_binarizeWithFixedThreshold(grayscale_matrix, threshold=best_threshold)
