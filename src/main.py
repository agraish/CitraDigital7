from pathlib import Path
from PIL import Image, ImageOps
import cv2
import numpy as np
import pytesseract
import re


# Lokasi Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# KONFIGURASI
# ============================================================

INPUT_FOLDER = Path("dataset/raw")

GROUND_TRUTH = "571012022000056"

# Area nomor ijazah
NUMBER_BOX = (
    167,
    2189,
    1058,
    2403
)

# Area tanda tangan
SIGNATURE_BOX = (
    300,
    1600,
    1500,
    2350
)

SIGNATURE_THRESHOLD = 2.0


# ============================================================
# FUNGSI OCR
# ============================================================

def extract_number(text):
    return "".join(re.findall(r"\d", text))


def read_number(gray):
    brightness = cv2.convertScaleAbs(
        gray,
        alpha=1.0,
        beta=30
    )

    text = pytesseract.image_to_string(
        brightness,
        config="--psm 7"
    ).strip()

    number = extract_number(text)

    return number


# ============================================================
# FUNGSI DETEKSI TANDA TANGAN
# ============================================================

def detect_signature(signature_image):

    gray = cv2.cvtColor(
        signature_image,
        cv2.COLOR_BGR2GRAY
    )

    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones(
        (3, 3),
        np.uint8
    )

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

    foreground = cv2.countNonZero(
        morphology
    )

    total_pixels = (
        morphology.shape[0]
        * morphology.shape[1]
    )

    percentage = (
        foreground
        / total_pixels
    ) * 100

    if percentage >= SIGNATURE_THRESHOLD:
        result = "PRESENT"
    else:
        result = "ABSENT"

    return result, percentage


# ============================================================
# PROSES SEMUA CITRA
# ============================================================

image_files = sorted(
    INPUT_FOLDER.glob("*.jpg")
)


for image_path in image_files:

    image = Image.open(image_path)

    # Memperbaiki orientasi berdasarkan EXIF
    image = ImageOps.exif_transpose(image)

    image_cv = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )


    # --------------------------------------------------------
    # AREA NOMOR IJAZAH
    # --------------------------------------------------------

    number_crop = image.crop(
        NUMBER_BOX
    )

    number_cv = cv2.cvtColor(
        np.array(number_crop),
        cv2.COLOR_RGB2BGR
    )

    number_gray = cv2.cvtColor(
        number_cv,
        cv2.COLOR_BGR2GRAY
    )

    number = read_number(
        number_gray
    )


    # --------------------------------------------------------
    # AREA TANDA TANGAN
    # --------------------------------------------------------

    signature_crop = image.crop(
        SIGNATURE_BOX
    )

    signature_cv = cv2.cvtColor(
        np.array(signature_crop),
        cv2.COLOR_RGB2BGR
    )

    signature_result, percentage = detect_signature(
        signature_cv
    )


    # --------------------------------------------------------
    # HASIL VERIFIKASI
    # --------------------------------------------------------

    number_valid = (
        number == GROUND_TRUTH
    )

    signature_valid = (
        signature_result == "PRESENT"
    )

    if number_valid and signature_valid:
        verification = "BERHASIL"
    else:
        verification = "TIDAK BERHASIL"


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print(image_path.name)
    print("=" * 60)

    print(
        "Nomor Ijazah :",
        number if number else "TIDAK TERBACA"
    )

    print(
        "Tanda Tangan :",
        signature_result
    )

    print(
        "Foreground   :",
        f"{percentage:.2f}%"
    )

    print(
        "Hasil Verifikasi :",
        verification
    )