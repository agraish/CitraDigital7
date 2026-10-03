from PIL import Image, ImageOps

image_path = "dataset/raw/01_HighQuality_Enhanced.jpg"

image = Image.open(image_path)

print("SIZE SEBELUM:", image.size)
print("EXIF ORIENTATION:", image.getexif().get(274))

oriented_image = ImageOps.exif_transpose(image)

print("SIZE SESUDAH:", oriented_image.size)

oriented_image.save("results/01_oriented.jpg")