import os
from app import FOLDER_IMAGE_NAME
from app.image_loader import ail_loadImgAsGrayscale
from app.utils import sysUtil_getImageList
# from random import randrange
from random import choice
import pytest
import io
from PIL import Image


def test_load_image_success_with_existing_file():
    folderName = FOLDER_IMAGE_NAME
    images = sysUtil_getImageList(folderName)
    assert images, f"No image files found in {folderName}"
    
    randomPath = choice(images)
    selectedPath = os.path.join(folderName, randomPath)
    grayScale = ail_loadImgAsGrayscale(selectedPath)
    
    assert isinstance(grayScale, list)
    assert len(grayScale) > 0
    assert all(isinstance(row, list) for row in grayScale)
    assert all(isinstance(px, int) for px in grayScale[0])
    assert 0 <= grayScale[0][0] <= 255    

def test_load_image_fail_not_an_image(tmp_path):
    fake = tmp_path / "fake.jpg"
    fake.write_text("this is not a real image")
    grayscale = ail_loadImgAsGrayscale(str(fake))
    assert grayscale == []
    
def test_load_image_small_sizes(tmp_path):
    img = Image.new("L", (2, 2), color=128)  # constant mid-gray
    p = tmp_path / "tiny.png"
    img.save(p)

    g = ail_loadImgAsGrayscale(str(p))
    assert len(g) == 2 and len(g[0]) == 2
    assert all(all(isinstance(px, int) for px in row) for row in g)
    assert all(px == 128 for row in g for px in row)    
    
def test_load_image_corrupted_file(tmp_path):
    corrupted = tmp_path / "broken.png"
    corrupted.write_bytes(b"\x89PNG\r\n\x1a\nBADBADBADBAD")  # invalid payload
    g = ail_loadImgAsGrayscale(str(corrupted))
    assert g == []    