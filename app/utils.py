import os

def sysUtil_printBinaryImage(maxtrix):
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
    imageFiles = [f for f in os.listdir(folder) if f.lower(). endswith(('.jpg', '.png'))]
    return sorted(imageFiles)
