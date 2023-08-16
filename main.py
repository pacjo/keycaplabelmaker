import os
import json
import argparse
from PIL import Image, ImageDraw, ImageColor, ImageOps
import cairosvg

parser = argparse.ArgumentParser(description="Quickly generate keycap lables")
parser.add_argument("json_file", help="Path to the JSON file containing icon data")
args = parser.parse_args()

# Helper function for coloring images
def hex_to_rgba(hex_color):
    # Convert hex color to RGB values
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Add alpha channel value (255 for fully opaque)
    rgba = rgb + (255,)

    return rgba

# Helper function for scaling images
def scale_image(image, main_width_pixels, main_height_pixels, scale):
    if scale == "quarter":
        return image.resize((int(main_width_pixels/2), int(main_height_pixels/2)))
    if scale in {"quarter", "half_vertical", "half_horizontal", }:
        return image.resize((int(main_width_pixels/2), int(main_height_pixels/2)))
    elif scale in {"full"}:
        return image.resize((main_width_pixels, main_height_pixels))
    else:
        print("No valid scale provided, skipping scaling")
        return image

# Constants
width_mm = 13       # Width in millimeters
height_mm = 13      # Height in millimeters
dpi = 96            # Dots per inch (96 is default for most PCs)
border_width = 1    # Border width in pixels

# Size of standard A4 page
paper_size_horizontal = 210
paper_size_vertical = 297

# Margins [mm] (failsafes for printing)
margin_horizontal = 6
margin_vertical = 6

max_labels_horizontal = int((paper_size_horizontal - 2 * margin_horizontal)/width_mm)
max_labels_vertical = int((paper_size_vertical - 2 * margin_vertical)/height_mm)

# Calculate main dimensions in pixels
main_width_pixels = int((width_mm / 25.4) * dpi)
main_height_pixels = int((height_mm / 25.4) * dpi)

# Prepare save path
if not os.path.exists("output"):
    os.makedirs("output")

with open(args.json_file, "r") as json_file:
    json_object = json.load(json_file)

    # Create image for label grid
    print(f'Number of keycaps: {len(json_object["keycaps"])}')
    label_grid = Image.new("RGBA", (max_labels_horizontal*main_width_pixels, int(len(json_object['keycaps'])/max_labels_vertical+1)*main_width_pixels), "white")

    for i in range(len(json_object['keycaps'])):
        # Create a new image with white background
        main_image = Image.new("RGBA", (main_width_pixels, main_height_pixels), json_object['metadata']['background_color'])

        # Draw a border around the image
        draw = ImageDraw.Draw(main_image)
        draw.rectangle(
            [(0, 0), (main_width_pixels - 1, main_height_pixels - 1)],
            outline=ImageColor.getcolor(json_object['metadata']['border_color'], "RGBA")
        )

        print(f'\nkeycap: {i}\nnumber of icons: {len(json_object["keycaps"][str(i)])}')

        for j in range(len(json_object["keycaps"][str(i)])):

            json_icon = json_object["keycaps"][str(i)][j]
            print(f'icon: {json_icon["icon"]}\nlocation: {json_icon["location"]}\ncolor: {json_icon["color"]}')

            # Open the icon, convert from svg if needed
            icon_path = f'icons/{json_icon["icon"][:json_icon["icon"].find(":")]}/{json_icon["icon"][json_icon["icon"].find(":")+1:]}'
            if not os.path.exists(f'{icon_path}.png'): cairosvg.svg2png(url=f'{icon_path}.svg', write_to=f'{icon_path}.png', output_width=256, output_height=256)
            icon = Image.open(f'{icon_path}.png')

            # Change icon's color according to json
            alpha = icon.getchannel('A')
            new_color = hex_to_rgba(json_icon["color"])
            icon_colorized = Image.new('RGBA', icon.size, new_color)
            icon_colorized.putalpha(alpha)

            # Resize and aste the second image onto the first one
            # (that's a lot of hard-coded trash, but I'm lazy)
            if json_icon["location"] in {"CC"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "full")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "full")
                main_image.paste(icon_colorized, (0, 0), icon)
            elif json_icon["location"] in {"CL", "LC"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "half_vertical")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "half_vertical")
                main_image.paste(icon_colorized, (0, int(main_height_pixels/4)), icon)
            elif json_icon["location"] in {"CR", "RC"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "half_vertical")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "half_vertical")
                main_image.paste(icon_colorized, (int(main_width_pixels/2), int(main_height_pixels/4)), icon)
            elif json_icon["location"] in {"CT", "TC"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "half_horizontal")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "half_horizontal")
                main_image.paste(icon_colorized, (int(main_width_pixels/4), 0), icon)
            elif json_icon["location"] in {"CB", "BC"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "half_horizontal")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "half_horizontal")
                main_image.paste(icon_colorized, (int(main_width_pixels/4), int(main_height_pixels/2)), icon)
            elif json_icon["location"] in {"TL", "LT"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "quarter")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "quarter")
                main_image.paste(icon_colorized, (0, 0), icon)
            elif json_icon["location"] in {"TR", "RT"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "quarter")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "quarter")
                main_image.paste(icon_colorized, (int(main_width_pixels/2), 0), icon)
            elif json_icon["location"] in {"BL", "LB"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "quarter")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "quarter")
                main_image.paste(icon_colorized, (0, int(main_height_pixels/2)), icon)
            elif json_icon["location"] in {"BR", "RB"}:
                icon = scale_image(icon, main_width_pixels, main_height_pixels, "quarter")
                icon_colorized = scale_image(icon_colorized, main_width_pixels, main_height_pixels, "quarter")
                main_image.paste(icon_colorized, (int(main_width_pixels/2), int(main_height_pixels/2)), icon)
            else:
                print("No location provided, skipping")

        # Add label to grid
        label_grid.paste(main_image, (i%max_labels_horizontal*main_width_pixels, int(i/max_labels_horizontal)*main_height_pixels))

        # Save the combined label
        main_image.save(f'output/keycap_{i}.png', dpi=(dpi, dpi))

    # Save label grid
    label_grid.save(f'output/grid.png', dpi=(dpi, dpi))
