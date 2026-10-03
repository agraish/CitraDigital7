from pathlib import Path
import cv2
import pytesseract
import re


# Lokasi Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Ground truth nomor ijazah
ground_truth = "571012022000056"

# Folder hasil enhancement
folders = {
    "Brightness": Path("results/numbers/brightness"),
    "Contrast Stretching": Path("results/numbers/contrast"),
    "Histogram Equalization": Path("results/numbers/histogram")
}


def extract_number(text):
    return "".join(re.findall(r"\d", text))


def levenshtein(a, b):
    rows = len(a) + 1
    cols = len(b) + 1

    distance = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        distance[i][0] = i

    for j in range(cols):
        distance[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            distance[i][j] = min(
                distance[i - 1][j] + 1,
                distance[i][j - 1] + 1,
                distance[i - 1][j - 1] + cost
            )

    return distance[-1][-1]


def calculate_cer(reference, prediction):
    if len(reference) == 0:
        return 0

    errors = levenshtein(reference, prediction)

    return errors / len(reference)


for method, folder in folders.items():

    print("\n" + "=" * 60)
    print("METODE:", method)
    print("=" * 60)

    image_files = sorted(folder.glob("*.jpg"))

    for image_path in image_files:

        image = cv2.imread(str(image_path))

        if image is None:
            continue

        config = "--psm 7"

        text = pytesseract.image_to_string(
            image,
            config=config
        ).strip()

        number = extract_number(text)

        cer = calculate_cer(
            ground_truth,
            number
        )

        print("\nGambar :", image_path.name)
        print("OCR    :", text)
        print("Nomor  :", number)
        print("CER    :", round(cer, 4))
        print("CER %  :", round(cer * 100, 2), "%")