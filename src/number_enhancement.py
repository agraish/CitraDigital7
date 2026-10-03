import cv2
import numpy as np

input_path = "results/01_number_gray.jpg"

gray = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

# ==================================================
# 1. BRIGHTNESS ADJUSTMENT
# ==================================================
brightness = cv2.convertScaleAbs(gray, alpha=1.0, beta=30)

cv2.imwrite(
    "results/01_number_brightness.jpg",
    brightness
)

# ==================================================
# 2. CONTRAST STRETCHING
# ==================================================
min_value = np.min(gray)
max_value = np.max(gray)

contrast_stretching = (
    (gray - min_value) * 255 / (max_value - min_value)
).astype(np.uint8)

cv2.imwrite(
    "results/01_number_contrast.jpg",
    contrast_stretching
)

# ==================================================
# 3. HISTOGRAM EQUALIZATION
# ==================================================
histogram_equalization = cv2.equalizeHist(gray)

cv2.imwrite(
    "results/01_number_histogram.jpg",
    histogram_equalization
)