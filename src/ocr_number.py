import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Nomor ijazah yang benar sebagai ground truth
ground_truth = "571012022000056"

images = {
    "Brightness": "results/01_number_brightness.jpg",
    "Contrast Stretching": "results/01_number_contrast.jpg",
    "Histogram Equalization": "results/01_number_histogram.jpg"
}


def calculate_cer(reference, prediction):
    m = len(reference)
    n = len(prediction)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if reference[i - 1] == prediction[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[m][n] / m


for method, path in images.items():

    image = cv2.imread(
        path,
        cv2.IMREAD_GRAYSCALE
    )

    text = pytesseract.image_to_string(
        image,
        config="--psm 7"
    )

    # Ambil hanya angka dari hasil OCR
    prediction = "".join(
        character for character in text
        if character.isdigit()
    )

    cer = calculate_cer(
        ground_truth,
        prediction
    )

    print("=" * 50)
    print("METODE :", method)
    print("OCR    :", text.strip())
    print("NOMOR  :", prediction)
    print("CER    :", round(cer, 4))
    print("CER %  :", round(cer * 100, 2), "%")