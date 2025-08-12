from app.image_binarizer import (
    aib_binarizeWithFixedThreshold,
    aib_binarizeWithOtsuThreshold,
)


def test_binarized_fixed_threshold_basic():
    gray = [
        [0, 64, 127, 128, 200, 255],
        [10, 120, 127, 129, 180, 254],
    ]

    binary = aib_binarizeWithFixedThreshold(gray, threshold=128)

    expected = [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
    ]
    assert binary == expected


def test_binarized_empty_returns_empty():
    empty_result = aib_binarizeWithFixedThreshold([], threshold=128)
    assert empty_result == []


def test_binarize_otsu_shape_and_range():
    gray = [
        [10, 10, 10, 10, 200, 200, 200, 200],
        [10, 10, 10, 10, 200, 200, 200, 200],
    ]
    binary = aib_binarizeWithOtsuThreshold(gray)

    assert len(binary) == len(gray)
    assert len(binary[0]) == len(gray[0])

    all_pixels_valid = all(pixel in (0, 1) for row in binary for pixel in row)
    assert all_pixels_valid
