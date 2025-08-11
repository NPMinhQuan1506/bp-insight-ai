from app.image_binarizer import aib_binarized, aib_binarized_otsu


def test_binarized_fixed_threshold_basic():
    g = [
        [0, 64, 127, 128, 200, 255],
        [10, 120, 127, 129, 180, 254],
    ]

    b = aib_binarized(g, threshold=128)

    assert b == [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
    ]


def test_binarized_empty_returns_empty():
    assert aib_binarized([], threshold=128) == []


def test_binarize_otsu_shape_and_range():
    g = [
        [10, 10, 10, 10, 200, 200, 200, 200],
        [10, 10, 10, 10, 200, 200, 200, 200],
    ]
    b = aib_binarized_otsu(g)
    assert len(b) == len(g)
    assert len(b[0]) == len(g[0])
    assert all(px in (0, 1) for row in b for px in row)
