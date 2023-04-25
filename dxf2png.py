import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file):
    dxf = ezdxf.readfile(input_file)
    msp = dxf.modelspace()
    extmin, extmax = msp.get_extents()
    width = abs(extmax[0] - extmin[0])
    height = abs(extmax[1] - extmin[1])
    png_width = 2048
    png_height = int(height / width * png_width)
    doc = freetype.Face(DEFAULT_FONT_PATH)
    font_size = int(png_width / 30)
    doc.set_char_size(size=font_size)
    with open(output_file, 'wb') as png_file:
        png_writer = png.Writer(png_width, png_height, greyscale=True)
        pixels = []
        for y in range(png_height):
            for x in range(png_width):
                p = get_point_from_pixel(x, y, png_width, png_height, extmin, extmax)
                if p is not None:
                    pixels.append(int(get_distance_to_nearest_entity(p, msp, doc) * 255))
        png_writer.write_array(png_file, pixels)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
