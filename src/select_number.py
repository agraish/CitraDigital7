import cv2
from PIL import Image, ImageOps

image_path = "dataset/raw/01_HighQuality_Enhanced.jpg"

# Buka gambar dan perbaiki orientasi berdasarkan EXIF
image = Image.open(image_path)
image = ImageOps.exif_transpose(image)

# Ubah PIL ke format OpenCV
image = cv2.cvtColor(
    __import__("numpy").array(image),
    cv2.COLOR_RGB2BGR
)

# Tampilkan gambar
window_name = "Pilih Area Nomor Ijazah"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1200, 800)

# Pilih area dengan mouse
x, y, w, h = cv2.selectROI(window_name, image, fromCenter=False)

cv2.destroyAllWindows()

# Tampilkan hasil koordinat
print("\nKOORDINAT AREA NOMOR IJAZAH")
print("LEFT   =", x)
print("TOP    =", y)
print("RIGHT  =", x + w)
print("BOTTOM =", y + h)

# Crop
crop = image[y:y+h, x:x+w]

# Simpan hasil crop
output_path = "results/01_number_crop.jpg"
cv2.imwrite(output_path, crop)

print("\nHasil crop disimpan di:")
print(output_path)