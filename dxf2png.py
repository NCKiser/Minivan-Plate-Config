import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file, width=800):
    dxf = ezdxf.readfile(input_file)
    modelspace = dxf.modelspace()
    extmax = dxf.header['$EXTMAX']
    extmin = dxf.header['$EXTMIN']
    x_min, y_min = extmin[0], extmin[1]
    x_max, y_max = extmax[0], extmax[1]
    width = int(width)
    height = int(width * ((y_max-y_min)/(x_max-x_min)))
    if height < 1:
        height = 1
    msp = dxf.modelspace()
    msp.transform_layout(msp.get_wcs_transformation() @ Matrix44.scale(sx=1.0, sy=1.0, sz=1.0))
    fig = Figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.axis('off')
    ax.set_aspect('equal')
    render = RenderContext(fig)
    render.add(msp, by_layer=True)
    result = Drawing.extract(render)
    result.image().save(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
