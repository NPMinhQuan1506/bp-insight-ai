import os
from app import APP_NAME, FOLDER_IMAGE_NAME, VERSION
from app.image_binarizer import aib_binarizeWithFixedThreshold
from app.image_loader import ail_loadImgAsGrayscale, ail_printGrayscalePreview
from app.utils import sysUtil_getImageList, sysUtil_printBinaryPreview


def am_runImageLoader(imagePath: str) -> None:
    grayscale: list[list[int]] = ail_loadImgAsGrayscale(imagePath)

    if not grayscale:
        print("Image loading failed")
    else:
        print("Image loaded successfully")
        ail_printGrayscalePreview(grayscale, limit=20)

        print("\n[Fixed threshold = 128]")
        b_fixed: list[list[int]] = aib_binarizeWithFixedThreshold(
            grayscale, threshold=128
        )
        sysUtil_printBinaryPreview(b_fixed, limit=60, rows=10)


def main() -> None:
    folderName: str = FOLDER_IMAGE_NAME

    while True:
        print("\n==============================")
        print(f"Welcome to {APP_NAME} version {VERSION}")
        print("Available images:")
        images: list[str] = sysUtil_getImageList(folderName)
        if not images:
            print(f"No image files found in {folderName}")
            return

        for idx, file in enumerate(images):
            print(f" [{idx}] {file}")

        print("  [x] Exit")
        print("==============================")

        userInput: str = input("Select image index (or 'x' to Exit): ").strip().lower()

        if userInput in ["x", "exit"]:
            print("See you again. Bye")
            break

        try:
            choice: int = int(userInput)
            if 0 <= choice < len(images):
                selectedImage: str = os.path.join(folderName, images[choice])
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
