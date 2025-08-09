import os
from app import FOLDER_IMAGE_NAME
from app.image_loader import ail_loadImgAsGrayscale
from app.utils import sysUtil_getImageList
from random import randrange
def til_testLoadImage_Success():
    folderName = FOLDER_IMAGE_NAME
    images = sysUtil_getImageList(folderName)
    if not images:
        assert False, f"No image files found in {folderName}"
    
    images = sysUtil_getImageList(folderName)
    randomPath = images[random(len(images) - 1)]
    grayScale = ail_loadImgAsGrayscale(randomPath)
    
    assert isinstance(grayScale, list)
    assert len(grayScale) > 0
    assert all(isinstance(row, list) for row in grayScale)
    assert all(isinstance(pixel, int) for pixels in grayScale[0])
    assert 0 <= grayscale[0][0] <= 255

    
def til_testLoadImage_Fail():
    path = "Image doesn't exist"
    grayScale = ail_loadImgAsGrayscale(path)
    assert grayscale == [], "Should return empty list on error"
    