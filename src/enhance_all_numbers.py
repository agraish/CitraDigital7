from pathlib import Path
import cv2
import numpy as np


input_folder = Path("results/numbers")

output_folders = {
    "grayscale": Path("results/numbers/grayscale"),
    "brightness": Path("results/numbers/brightness"),
    "contrast": Path("results/numbers/contrast"),
    "histogram": Path("results/numbers/histogram")
}

for folder in output_folders.values():
    folder.mkdir(parents=True, exist_ok=True)


crop_files = sorted(input_folder.glob("*_number_crop.jpg"))


for image_path in crop_files:

    image = cv2.imread(str(image_path))

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Brightness Adjustment
    brightness = cv2.convertScaleAbs(
        gray,
        alpha=1.0,
        beta=30
    )

    # Contrast Stretching
    min_value = np.min(gray)
    max_value = np.max(gray)

    if max_value > min_value:
        contrast = (
            (gray - min_value)
            * 255
            / (max_value - min_value)
        ).astype(np.uint8)
    else:
        contrast = gray.copy()

    # Histogram Equalization
    histogram = cv2.equalizeHist(gray)

    filename = image_path.stem + ".jpg"

    cv2.imwrite(
        str(output_folders["grayscale"] / filename),
        gray
    )

    cv2.imwrite(
        str(output_folders["brightness"] / filename),
        brightness
    )

    cv2.imwrite(
        str(output_folders["contrast"] / filename),
        contrast
    )

    cv2.imwrite(
        str(output_folders["histogram"] / filename),
        histogram
    )


print("Jumlah crop yang diproses:", len(crop_files))