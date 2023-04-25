import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    modelspace = doc.modelspace()
    extmin = doc.header['$EXTMIN']
    extmax = doc.header['$EXTMAX']
    x_min, y_min = extmin[0], extmin[1]
    x_max, y_max = extmax[0], extmax[1]
    width, height = int((x_max - x_min) * SCALE), int((y_max - y_min) * SCALE)
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    for entity in modelspace:
        if entity.dxftype() == "LINE":
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            start_point = ((start_point[0] - x_min) * SCALE, height - (start_point[1] - y_min) * SCALE)
            end_point = ((end_point[0] - x_min) * SCALE, height - (end_point[1] - y_min) * SCALE)
            draw.line([start_point, end_point], fill="black", width=2)

    image.save(output_file, "PNG")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
