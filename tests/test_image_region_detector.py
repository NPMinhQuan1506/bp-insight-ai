from app.region_detector import adr_detectRegions


def test_detect_simple_regions():
    matrix = [
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 1],
    ]
    expected = [(1, 0, 2, 2), (4, 1, 2, 2)]
    result = adr_detectRegions(matrix, min_height=1, min_width=1)
    assert result == expected


def test_detect_complex_shape():
    matrix = [
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ]
    expected = [(0, 0, 3, 3)]
    result = adr_detectRegions(matrix, min_height=1, min_width=1)
    assert result == expected


def test_filtering_and_sorting():
    matrix = [
        [0, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
    ]
    expected_sorted = [(2, 2, 2, 2), (4, 0, 2, 2)]
    result = adr_detectRegions(matrix, min_height=2, min_width=2)
    assert result == expected_sorted


def test_empty_image():
    matrix = []
    assert adr_detectRegions(matrix) == []


def test_image_with_no_regions():
    matrix = [
        [0, 0, 0],
        [0, 0, 0],
    ]
    assert adr_detectRegions(matrix) == []
