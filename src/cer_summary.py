from pathlib import Path
import cv2
import pytesseract
import re


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

ground_truth = "571012022000056"

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
    return levenshtein(reference, prediction) / len(reference)


summary = {}

for method, folder in folders.items():

    cer_values = []

    for image_path in sorted(folder.glob("*.jpg")):

        image = cv2.imread(str(image_path))

        text = pytesseract.image_to_string(
            image,
            config="--psm 7"
        ).strip()

        number = extract_number(text)

        cer = calculate_cer(
            ground_truth,
            number
        )

        cer_values.append(cer)

    average_cer = sum(cer_values) / len(cer_values)

    summary[method] = average_cer


print("\nREKAP HASIL CER")
print("=" * 50)

for method, cer in summary.items():
    print(
        f"{method:<25} "
        f"CER rata-rata: {cer:.4f} "
        f"({cer * 100:.2f}%)"
    )