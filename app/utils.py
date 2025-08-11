import os


def sysUtil_printBinaryImage(matrix):
    for row in matrix:
        print("".join(" " if pixel == 1 else " " for pixel in row))


def sysUtil_resizeMatrix(matrix, newWidth, newHeight):
    pass


def sysUtil_getImageList(folder="input_images"):
    """_summary_

    Args:
        folder (str, optional): _description_. Defaults to FOLDER_IMAGE_NAME.

    Returns:
        List all .jpg and .png files in the given folder
    """
    imageFiles = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".png"))]
    return sorted(imageFiles)


def sysUtil_printBinaryPreview(binaryMatrix, limit=60, rows=10):
    if not binaryMatrix:
        print("[INFO] Empty binary matrix.")
        return

    height = min(rows, len(binaryMatrix))
    width = min(limit, len(binaryMatrix[0]))
    print(f"Binary preview (rows={height}, cols={width}):")

    for y in range(height):
        line = "".join(" " if binaryMatrix[y][x] == 1 else " " for x in range(width))
        print(line)
