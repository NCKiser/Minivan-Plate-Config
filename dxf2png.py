import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file):
    dxf = ezdxf.readfile(input_file)
    msp = dxf.modelspace()
    extmin, extmax = msp.max_limits()
    width = int((extmax[0] - extmin[0]) * DPI)
    height = int((extmax[1] - extmin[1]) * DPI)
    dwg = ezdxf.new('AC1009')
    image = ezdxf.render.Image((width, height), background=COLOR_BG)
    dwg.modelspace().add_image(image, insert=(0, 0))
    ms = dwg.modelspace()
    ms.add_blockref('IMAGE', (0, 0))
    ms.add_image_def('IMAGE', image=image, size_in_pixel=image.size, transparency=0)
    dwg.saveas(output_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
