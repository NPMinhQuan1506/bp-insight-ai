import os
from app import FOLDER_IMAGE_NAME
from app.image_loader import ail_loadImgAsGrayscale
from app.utils import sysUtil_getImageList
# from random import randrange
from random import choice
def test_LoadImage_Success():
    folderName = FOLDER_IMAGE_NAME
    images = sysUtil_getImageList(folderName)
    if not images:
        assert False, f"No image files found in {folderName}"
    
    randomPath = choice(images)
    selectedPath = os.path.join(folderName, randomPath)
    grayScale = ail_loadImgAsGrayscale(selectedPath)
    assert isinstance(grayScale, list)
    assert len(grayScale) > 0
    assert all(isinstance(row, list) for row in grayScale)
    assert all(isinstance(px, int) for px in grayScale[0])
    assert 0 <= grayScale[0][0] <= 255

    
def test_LoadImage_Fail():
    path = "Image doesn't exist"
    grayScale = ail_loadImgAsGrayscale(path)
    assert grayScale == [], "Should return empty list on error"
    