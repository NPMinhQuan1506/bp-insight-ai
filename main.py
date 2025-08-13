import os
import itertools
from app import APP_NAME, FOLDER_IMAGE_NAME, VERSION
from app.image_binarizer import (
    aib_binarizeWithFixedThreshold,
    aib_binarizeWithOtsuThreshold,
)
from app.image_region_detector import adr_detectRegions
from app.image_loader import ail_loadImgAsGrayscale, ail_printGrayscalePreview
from app.image_denoiser import aid_applyGaussianBlur
from app.utils import sysUtil_getImageList, sysUtil_printBinaryPreview


def am_autoChooseParams(grayScale):
    kernel_sizes = [3, 5, 7]
    sigmas = [round(x, 2) for x in [0.8, 1.0, 1.2, 1.5, 2.0]]
    best_score = -1
    best_params = (3, 1.0)
    best_binary = None

    for kernel, sigma in itertools.product(kernel_sizes, sigmas):
        try:
            denoised = aid_applyGaussianBlur(grayScale, kernelSize=kernel, sigma=sigma)
            binary = aib_binarizeWithOtsuThreshold(denoised)
            flat = [px for row in binary for px in row]
            if not flat:
                continue
            mean = sum(flat) / len(flat)
            score = 1 - abs(mean - 0.5)
            if score > best_score:
                best_score = score
                best_params = (kernel, sigma)
                best_binary = binary
        except Exception:
            continue

    return best_params, best_binary


def am_runImageLoader(imagePath):
    grayscale = ail_loadImgAsGrayscale(imagePath)

    if not grayscale:
        print("Image loading failed")
    else:
        print("Image loaded successfully")
        ail_printGrayscalePreview(grayscale, limit=20)
        (kernel, sigma), binary = am_autoChooseParams(grayscale)
        print(f"Auto-selected GaussianBlur: kernelSize={kernel}, sigma={sigma}")

        sysUtil_printBinaryPreview(binary, limit=60, rows=10)
        regions = adr_detectRegions(binary)
        print(f"Detected {len(regions)} regions (bounding boxes):")
        for idx, (x, y, w, h) in enumerate(regions):
            print(f"  Region {idx+1}: x={x}, y={y}, w={w}, h={h}")


def main():
    folderName = FOLDER_IMAGE_NAME

    while True:
        print("\n==============================")
        print(f"Welcome to {APP_NAME} version {VERSION}")
        print("Available images:")
        images = sysUtil_getImageList(folderName)
        if not images:
            print(f"No image files found in {folderName}")
            return

        for idx, file in enumerate(images):
            print(f" [{idx}] {file}")

        print("  [x] Exit")
        print("==============================")

        userInput = input("Select image index (or 'x' to Exit): ").strip().lower()

        if userInput in ["x", "exit"]:
            print("See you again. Bye")
            break

        try:
            choice = int(userInput)
            if 0 <= choice < len(images):
                selectedImage = os.path.join(folderName, images[choice])
                print(f"Loading image: {selectedImage}")
                am_runImageLoader(selectedImage)
            else:
                print(f" Invalid index. Range from 0 to {len(images) - 1}")
        except ValueError:
            print("Enter a valid number")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user (Ctrl + C).")
