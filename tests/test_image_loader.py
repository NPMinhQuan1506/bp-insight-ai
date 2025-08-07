import os
from . import FOLDER_IMAGE_NAME
from app.image_loader import ail_loadImgAsGrayscale
from app.utils import sysUtil_getImageList

def til_testLoadImage_Success():
    folderName = FOLDER_IMAGE_NAME
    images = sysUtil_getImageList(folderName)
    if not images:
        assert False, f"No image files found in {folderName}"
    
    