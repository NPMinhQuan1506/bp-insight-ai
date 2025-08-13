import pytest

from test_image_denoiser import aid_applyGaussianBlur


def test_empty_matrix():
    assert aid_applyGaussianBlur([]) == []
    assert aid_applyGaussianBlur([[]]) == []


def test_invalid_kernel_size():
    matrix = [[100, 150, 200], [50, 75, 125], [0, 50, 100]]
    with pytest.raises(ValueError):
        aid_applyGaussianBlur(matrix, kernelSize=4, sigma=1.0)


def test_single_pixel():
    matrix = [[123]]
    result = aid_applyGaussianBlur(matrix, kernelSize=3, sigma=1.0)
    assert result == [[123]]


def test_small_matrix_sigma1():
    matrix = [[0, 50, 100], [150, 200, 250], [30, 60, 90]]
    result = aid_applyGaussianBlur(matrix, kernelSize=3, sigma=1.0)

    assert len(result) == 3
    assert all(len(row) == 3 for row in result)
    assert 0 <= min(min(row) for row in result) <= 255
    assert 0 <= max(max(row) for row in result) <= 255


def test_large_sigma_blur():
    matrix = [[0, 255, 0], [255, 0, 255], [0, 255, 0]]
    result_small_sigma = aid_applyGaussianBlur(matrix, kernelSize=3, sigma=0.5)
    result_large_sigma = aid_applyGaussianBlur(matrix, kernelSize=3, sigma=5.0)

    range_small = max(max(row) for row in result_small_sigma) - min(
        min(row) for row in result_small_sigma
    )
    range_large = max(max(row) for row in result_large_sigma) - min(
        min(row) for row in result_large_sigma
    )

    assert range_large < range_small


def test_rectangular_matrix():
    matrix = [[10, 20, 30, 40], [50, 60, 70, 80]]
    result = aid_applyGaussianBlur(matrix, kernelSize=3, sigma=1.0)
    assert len(result) == 2
    assert all(len(row) == 4 for row in result)


def test_kernel_size_5():
    matrix = [
        [0, 0, 0, 0, 0],
        [0, 255, 255, 255, 0],
        [0, 255, 255, 255, 0],
        [0, 255, 255, 255, 0],
        [0, 0, 0, 0, 0],
    ]
    result = aid_applyGaussianBlur(matrix, kernelSize=5, sigma=1.5)
    assert len(result) == 5
    assert all(len(row) == 5 for row in result)
    assert 0 <= min(min(row) for row in result) <= 255
    assert 0 <= max(max(row) for row in result) <= 255
