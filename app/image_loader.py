from PIL import Image

def ail_loadImgAsGrayscale(imagePath):
    """
    Load an image file and convert it to a 2D grayscale matrix.

    Args:
        imagePath (str): Path to the image file (.jpg, .png, etc.)

    Returns:
        list[list[int]]: 2D matrix of pixel values (0-255 grayscale)
    """

    try:
        #Open the image and convert to 8-bit grayscale mode ('L')
        image = Image.open(imagePath).convert('L')
    except Exception as error:
        print(f"loadImgAsGrayscale [ERROR] Failted to open image: {imagePath}")
        print(error)
        return []
    
    width, height = image.size
    grayscaleMatrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixelValue = image.getpixel((x, y))
            row.append(pixelValue)
        grayscaleMatrix.append(row)
        
    return grayscaleMatrix

def ail_printGrayscale_Preview(grayscaleMatrix, limit = 10):
    """_summary_

    Args:
        grayscaleMatrix (_type_): _description_
        limit (int, optional): _description_. Defaults to 10.
    """
    if not grayscaleMatrix:
        print("printGrayscale [INFO] Emptry matrix")
        return
    
    print(f"Matrix dimensions: {len(grayscaleMatrix)} rows x {len(grayscaleMatrix[0])} columns")
    print("printGrayscale [Preview]")
    
    for row in grayscaleMatrix[:5]:
        print(" ".join(f"{val: 3}" for val in row[:limit]))

    