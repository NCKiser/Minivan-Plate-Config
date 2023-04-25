import os
import sys
import ezdxf
from PIL import Image

def convert_dxf_to_png(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()
    bbox = msp.get_bbox()
    width = int(bbox.width)
    height = int(bbox.height)
    dwg_image = Image.new("RGB", (width, height), "white")
    modelspace = doc.modelspace()
    for entity in modelspace:
        if entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            x1 = int(start_point[0])
            y1 = int(start_point[1])
            x2 = int(end_point[0])
            y2 = int(end_point[1])
            dwg_image.putpixel((x1, y1), (0, 0, 0))
            dwg_image.putpixel((x2, y2), (0, 0, 0))
    dwg_image.save(output_file)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_dxf_to_png(input_file, output_file)
