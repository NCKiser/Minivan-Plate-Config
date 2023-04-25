import os
import dxfgrabber
from PIL import Image

# Path to the folder containing the input DXF files
input_folder = "all_dxf/"

# Path to the folder where the output PNG files will be saved
output_folder = "all_preview/"

# Create the output folder if it does not already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the DXF files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".dxf"):
        # Load the DXF file
        dxf = dxfgrabber.readfile(input_folder + filename)

        # Get the bounding box of the drawing
        x_min, y_min, x_max, y_max = dxf.header['$EXTMIN'], dxf.header['$EXTMAX']

        # Calculate the width and height of the drawing in pixels
        width = int((x_max - x_min) * 100)
        height = int((y_max - y_min) * 100)

        # Create a new image with the calculated dimensions
        img = Image.new("RGB", (width, height), color=(255, 255, 255))

        # Draw the entities in the drawing onto the image
        for entity in dxf.entities:
            if entity.dxftype == 'LINE':
                x1 = int((entity.start[0] - x_min) * 100)
                y1 = int((entity.start[1] - y_min) * 100)
                x2 = int((entity.end[0] - x_min) * 100)
                y2 = int((entity.end[1] - y_min) * 100)
                img_draw = ImageDraw.Draw(img)
                img_draw.line([(x1, height - y1), (x2, height - y2)], fill=(0, 0, 0), width=1)

        # Save the image as a PNG file
        output_filename = os.path.splitext(filename)[0] + ".png"
        img.save(output_folder + output_filename)

        print(f"{filename} converted to {output_filename}")

print("Conversion complete.")
