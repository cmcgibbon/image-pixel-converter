# Command Line Image to Pixel Image Converter
from pathlib import Path
import math
from PIL import Image
from simple_term_menu import TerminalMenu

path_to_image = input("Path To Image: ").strip("'")

file_name = Path(path_to_image).name

resolutions = ["0.25x", "0.0625x", "0.00390625x", "0.00001525878x"]

terminal_menu = TerminalMenu(resolutions, title="Select a resolution: ")
selected_index = terminal_menu.show()

if selected_index is not None:
    with Image.open(path_to_image) as img:
        img = img.convert("RGBA")
        width, height = img.size
        # Cut off rightmost or bottom strip if image is uneven to ensure complete pixels
        if selected_index == 0:
            block = 2
        elif selected_index == 1:
            block = 4
        elif selected_index == 2:
            block = 16
        else:
            block = 256
        width -= width % block
        height -= height % block
        img_copy = img.crop((0, 0, width, height))

        pixels = img_copy.load()
        match selected_index:
            case 0:
                for x in range(0, width, 2):
                    for y in range(0, height, 2):
                        cluster = [pixels[x, y], pixels[x+1, y], pixels[x, y+1], pixels[x+1,y+1]]

                        red_sq, green_sq, blue_sq, alpha_sum = 0, 0, 0, 0

                        # Weight colours by alpha for transparent pixels
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
                            alpha_avg = round(alpha_sum / 4)
                            new_px = (red_avg, green_avg, blue_avg, alpha_avg)

                        for cx in range(x, x + 2):
                            for cy in range(y, y + 2):
                                pixels[cx, cy] = new_px
                
                if len(file_name.split(".")) == 2:
                    file, ext = file_name.split(".")
                else:
                    i = len(file_name) - 1
                    while file_name[i] != ".":
                        i -= 1
                    file, ext = file_name[:i], file_name[i+1:]
                
                new_filename = f"{file}-pixelated-0.25x.{ext}"

                img_copy.save(new_filename)

            case 1:
                for x in range(0, width, 4):
                    for y in range(0, height, 4):

                        cluster = []
                        for cx in range(x, x + 4):
                            for cy in range(y, y + 4):
                                cluster.append(pixels[cx, cy])

                        red_sq, green_sq, blue_sq, alpha_sum = 0, 0, 0, 0

                        for px in cluster:
                            red_sq += px[0]**2 * px[3]
                            green_sq += px[1]**2 * px[3]
                            blue_sq += px[2]**2 * px[3]
                            alpha_sum += px[3]

                        if alpha_sum == 0:
                            new_px = (0, 0, 0, 0)
                        else:
                            red_avg = round(math.sqrt(red_sq / alpha_sum))
                            green_avg = round(math.sqrt(green_sq / alpha_sum))
                            blue_avg = round(math.sqrt(blue_sq / alpha_sum))
                            alpha_avg = round(alpha_sum / 4)
                            new_px = (red_avg, green_avg, blue_avg, alpha_avg)

                        for cx in range(x, x + 4):
                            for cy in range(y, y + 4):
                                pixels[cx, cy] = new_px
                
                if len(file_name.split(".")) == 2:
                    file, ext = file_name.split(".")
                else:
                    i = len(file_name) - 1
                    while file_name[i] != ".":
                        i -= 1
                    file, ext = file_name[:i], file_name[i+1:]
                
                new_filename = f"{file}-pixelated-0.0625x.{ext}"

                img_copy.save(new_filename)

            case 2:
                for x in range(0, width, 16):
                    for y in range(0, height, 16):

                        cluster = []
                        for cx in range(x, x + 16):
                            for cy in range(y, y + 16):
                                cluster.append(pixels[cx, cy])

                        red_sq, green_sq, blue_sq, alpha_sum = 0, 0, 0, 0

                        for px in cluster:
                            red_sq += px[0]**2 * px[3]
                            green_sq += px[1]**2 * px[3]
                            blue_sq += px[2]**2 * px[3]
                            alpha_sum += px[3]

                        if alpha_sum == 0:
                            new_px = (0, 0, 0, 0)
                        else:
                            red_avg = round(math.sqrt(red_sq / alpha_sum))
                            green_avg = round(math.sqrt(green_sq / alpha_sum))
                            blue_avg = round(math.sqrt(blue_sq / alpha_sum))
                            alpha_avg = round(alpha_sum / 4)
                            new_px = (red_avg, green_avg, blue_avg, alpha_avg)

                        for cx in range(x, x + 16):
                            for cy in range(y, y + 16):
                                pixels[cx, cy] = new_px
                
                if len(file_name.split(".")) == 2:
                    file, ext = file_name.split(".")
                else:
                    i = len(file_name) - 1
                    while file_name[i] != ".":
                        i -= 1
                    file, ext = file_name[:i], file_name[i+1:]
                
                new_filename = f"{file}-pixelated-0.00390625x.{ext}"

                img_copy.save(new_filename)
              
            case 3:
                for x in range(0, width, 256):
                    for y in range(0, height, 256):

                        cluster = []
                        for cx in range(x, x + 256):
                            for cy in range(y, y + 256):
                                cluster.append(pixels[cx, cy])

                        red_sq, green_sq, blue_sq, alpha_sum = 0, 0, 0, 0

                        for px in cluster:
                            red_sq += px[0]**2 * px[3]
                            green_sq += px[1]**2 * px[3]
                            blue_sq += px[2]**2 * px[3]
                            alpha_sum += px[3]

                        if alpha_sum == 0:
                            new_px = (0, 0, 0, 0)
                        else:
                            red_avg = round(math.sqrt(red_sq / alpha_sum))
                            green_avg = round(math.sqrt(green_sq / alpha_sum))
                            blue_avg = round(math.sqrt(blue_sq / alpha_sum))
                            alpha_avg = round(alpha_sum / 4)
                            new_px = (red_avg, green_avg, blue_avg, alpha_avg)

                        for cx in range(x, x + 256):
                            for cy in range(y, y + 256):
                                pixels[cx, cy] = new_px
                
                if len(file_name.split(".")) == 2:
                    file, ext = file_name.split(".")
                else:
                    i = len(file_name) - 1
                    while file_name[i] != ".":
                        i -= 1
                    file, ext = file_name[:i], file_name[i+1:]
                
                new_filename = f"{file}-pixelated-0.00001525878x.{ext}"

                img_copy.save(new_filename)

else:
    raise ValueError("Must select resolution")