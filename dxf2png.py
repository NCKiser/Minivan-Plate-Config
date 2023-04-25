import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file):
    dxf = ezdxf.readfile(input_file)
    modelspace = dxf.modelspace()

    if '$EXTMIN' in dxf.header:
        x_min, y_min, _ = dxf.header['$EXTMIN']
    else:
        x_min, y_min = 0, 0

    if '$EXTMAX' in dxf.header:
        x_max, y_max, _ = dxf.header['$EXTMAX']
    else:
        x_max, y_max = 100, 100

    # scale factor to fit drawing within a 1024x1024 image
    scale_factor = 1024 / max(x_max - x_min, y_max - y_min)

    # create a new DXF drawing with scaled entities
    scaled_dxf = ezdxf.new('R2010')
    msp = scaled_dxf.modelspace()
    for entity in modelspace:
        msp.add_entity(entity.copy().scale(scale_factor))

    # save the drawing to a PNG file
    scaled_dxf.saveas(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
