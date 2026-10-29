# Command Line Image to Pixel Image Converter
from pathlib import Path
import math
from PIL import Image

path_to_image = input("Path To Image: ").strip("'")

file_name = Path(path_to_image).name

while True:
    try:
        size_of_pixel = int(input("Size Of Pixel (Number): "))
        break
    except ValueError:
        print("Please enter a whole number")

def pixelate(img: Image, pixel_size: int) -> None:
    img = img.convert("RGBA")
    width, height = img.size

    if pixel_size < 1 or pixel_size > width or pixel_size > height:
        raise ValueError("Pixel size must be within native resolution")
    # Cut off rightmost or bottom strip if image is uneven to ensure complete pixels
    width -= width % pixel_size
    height -= height % pixel_size
    img_copy = img.crop((0, 0, width, height))

    pixels = img_copy.load()

    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):

            cluster = []
            for cx in range(x, x + pixel_size):
                for cy in range(y, y + pixel_size):
                    cluster.append(pixels[cx, cy])
            
            red_sq, green_sq, blue_sq, alpha_sum = 0, 0, 0, 0

            # Weight colors by alpha for transparent pixels
            for px in cluster:
                red_sq += px[0]**2 * px[3]
                green_sq += px[1]**2 * px[3]
                blue_sq += px[2]**2 * px[3]
                alpha_sum += px[3]

            if alpha_sum == 0:
                new_px = (0, 0, 0, 0)
            else:
                # Perceptually accurate average
                red_avg = round(math.sqrt(red_sq / alpha_sum))
                green_avg = round(math.sqrt(green_sq / alpha_sum))
                blue_avg = round(math.sqrt(blue_sq / alpha_sum))
                # Pixels are either there or not
                if alpha_sum / (pixel_size**2) >= 128:
                    alpha_avg = 255
                else:
                    alpha_avg = 0
                new_px = (red_avg, green_avg, blue_avg, alpha_avg)

            for cx in range(x, x + pixel_size):
                for cy in range(y, y + pixel_size):
                    pixels[cx, cy] = new_px

    if len(file_name.split(".")) == 2:
        file, ext = file_name.split(".")
    else:
        i = len(file_name) - 1
        while file_name[i] != ".":
            i -= 1
        file, ext = file_name[:i], file_name[i+1:]
    
    new_filename = f"{file}-pixelated.{ext}"

    img_copy.save(new_filename)

with Image.open(path_to_image) as img:
    pixelate(img, size_of_pixel)