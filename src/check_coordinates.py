from PIL import Image, ImageOps, ImageDraw

image_path = "dataset/raw/01_HighQuality_Enhanced.jpg"

image = Image.open(image_path)
image = ImageOps.exif_transpose(image)

draw = ImageDraw.Draw(image)

width, height = image.size

# Garis vertikal setiap 250 pixel
for x in range(0, width, 250):
    draw.line((x, 0, x, height), fill="red", width=2)
    draw.text((x + 5, 5), str(x), fill="red")

# Garis horizontal setiap 250 pixel
for y in range(0, height, 250):
    draw.line((0, y, width, y), fill="red", width=2)
    draw.text((5, y + 5), str(y), fill="red")

image.save("results/01_coordinate.jpg")