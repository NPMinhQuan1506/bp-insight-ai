from PIL import Image


def ail_loadImgAsGrayscale(img_path):
    """
    Load an image file and convert it to a 2D grayscale matrix.

    Args:
        img_path (str): Path to the image file (.jpg, .png, etc.)

    Returns:
        list[list[int]]: 2D matrix of pixel values (0-255 grayscale)
    """

    try:
        # Open the image and convert to 8-bit grayscale mode ('L')
        img = Image.open(img_path).convert("L")
    except Exception as error:
        print(f"loadImgAsGrayscale [ERROR] Failed to open image: {img_path}")
        print(error)
        return []

    width, height = img.size
    gray_matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = img.getpixel((x, y))
            row.append(pixel)
        gray_matrix.append(row)

    return gray_matrix


def ail_printGrayscalePreview(gray_matrix, limit=10):
    """
    Print a preview of the grayscale matrix.

    Args:
        gray_matrix (list[list[int]]): 2D grayscale matrix
        limit (int, optional): Number of columns to show. Defaults to 10.
    """
    if not gray_matrix:
        print("printGrayscale [INFO] Empty matrix")
        return

    rows = len(gray_matrix)
    cols = len(gray_matrix[0])
    print(f"Matrix dimensions: {rows} rows x {cols} columns")
    print("printGrayscale [Preview]")

    preview_rows = gray_matrix[:5]
    for row in preview_rows:
        preview_cols = row[:limit]
        formatted_row = " ".join(f"{val:3}" for val in preview_cols)
        print(formatted_row)
