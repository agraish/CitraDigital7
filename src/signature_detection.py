from pathlib import Path
from PIL import Image, ImageOps
import cv2
import numpy as np


input_folder = Path("dataset/raw")
output_folder = Path("results/signatures")

output_folder.mkdir(parents=True, exist_ok=True)


# Koordinat area tanda tangan
LEFT = 300
TOP = 1600
RIGHT = 1500
BOTTOM = 2350


image_files = sorted(input_folder.glob("*.jpg"))


for image_path in image_files:

    # Membuka dan memperbaiki orientasi berdasarkan EXIF
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)

    # Crop area tanda tangan
    signature_crop = image.crop(
        (LEFT, TOP, RIGHT, BOTTOM)
    )

    # Konversi PIL ke OpenCV
    image_cv = cv2.cvtColor(
        np.array(signature_crop),
        cv2.COLOR_RGB2BGR
    )

    # Grayscale
    gray = cv2.cvtColor(
        image_cv,
        cv2.COLOR_BGR2GRAY
    )

    # Thresholding Otsu
    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Morphology untuk membersihkan noise
    kernel = np.ones((3, 3), np.uint8)

    morphology = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    morphology = cv2.morphologyEx(
        morphology,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=1
    )

    # Hitung jumlah piksel foreground
    foreground = cv2.countNonZero(morphology)

    total_pixels = morphology.shape[0] * morphology.shape[1]

    percentage = (
        foreground / total_pixels
    ) * 100

    # Threshold keputusan
    if percentage >= 2.0:
        result = "PRESENT"
    else:
        result = "ABSENT"

    # Simpan hasil crop
    filename = image_path.stem

    cv2.imwrite(
        str(output_folder / f"{filename}_signature_crop.jpg"),
        image_cv
    )

    cv2.imwrite(
        str(output_folder / f"{filename}_gray.jpg"),
        gray
    )

    cv2.imwrite(
        str(output_folder / f"{filename}_threshold.jpg"),
        binary
    )

    cv2.imwrite(
        str(output_folder / f"{filename}_morphology.jpg"),
        morphology
    )

    print(
        f"{image_path.name} -> "
        f"{result} | "
        f"Foreground: {foreground} | "
        f"Percentage: {percentage:.2f}%"
    )