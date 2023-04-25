import os
import argparse
import ezdxf
from PIL import Image

def convert_dxf_to_png(input_file, output_file):
    # Load the DXF file
    doc = ezdxf.readfile(input_file)

    # Get the Modelspace
    msp = doc.modelspace()

    # Get the bounding box of the Modelspace
    bbox = msp.bbox()

    # Calculate the size of the PNG image
    width = int(bbox.width)
    height = int(bbox.height)

    # Create a new PIL image
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

    # Create a PIL drawing context
    drawing = ImageDraw.Draw(image)

    # Iterate over all entities in the Modelspace
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            drawing.line((start[0], height - start[1], end[0], height - end[1]), fill=(0, 0, 0, 255))

    # Save the image to disk
    image.save(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a DXF file to PNG.')
    parser.add_argument('input_file', metavar='INPUT_FILE', help='the DXF file to convert')
    parser.add_argument('output_file', metavar='OUTPUT_FILE', help='the PNG file to create')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
