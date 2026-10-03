from pathlib import Path
from PIL import Image, ImageOps


input_folder = Path("dataset/raw")
output_folder = Path("results/numbers")

output_folder.mkdir(parents=True, exist_ok=True)


# Koordinat area nomor ijazah
LEFT = 167
TOP = 2189
RIGHT = 1058
BOTTOM = 2403


image_files = sorted(input_folder.glob("*.jpg"))

for image_path in image_files:

    print("Memproses:", image_path.name)

    image = Image.open(image_path)

    # Perbaiki orientasi berdasarkan EXIF
    image = ImageOps.exif_transpose(image)

    # Crop area nomor
    number_crop = image.crop(
        (LEFT, TOP, RIGHT, BOTTOM)
    )

    output_path = output_folder / (
        image_path.stem + "_number_crop.jpg"
    )

    number_crop.save(output_path)

print("\nTotal gambar diproses:", len(image_files))