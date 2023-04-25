import os
import re
import sys
import glob
import argparse
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


class DXF2IMG(object):

    default_img_format = '.png'
    default_img_res = 300

    def __init__(self, img_format=default_img_format, img_res=default_img_res):
        self.img_format = img_format
        self.img_res = img_res

    def convert_dxf2img(self, names):
        for name in names:
            # Check if a PNG file with the same name already exists in the 'all_preview' folder
            png_name = os.path.join('all_preview', os.path.splitext(os.path.basename(name))[0] + self.img_format)
            if os.path.isfile(png_name):
                print(f'{png_name} already exists, skipping conversion...')
                continue

            try:
                doc = ezdxf.readfile(name)
            except IOError as e:
                print(f'Error: Could not read DXF file {name}: {e}', file=sys.stderr)
                continue

            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                print(f'Error: DXF file {name} is damaged and cannot be converted', file=sys.stderr)
                continue

            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(doc)
            ctx.set_current_layout(msp)
            # ctx.current_layout.set_colors(bg='#FFFFFF')
            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(msp, finalize=True)

            first_param = re.sub(r'\.dxf$', self.img_format, os.path.basename(name))
            png_path = os.path.join('all_preview', first_param)
            try:
                fig.savefig(png_path, dpi=self.img_res)
            except IOError as e:
                print(f'Error: Could not save PNG file {png_path}: {e}', file=sys.stderr)
                continue

            print(f'Converted {name} to {png_path}')

def main():
    parser = argparse.ArgumentParser(description='Convert DXF files to PNG')
    parser.add_argument('dxf_dir', help='Path to the directory containing DXF files')
    parser.add_argument('--img-format', default=DXF2IMG.default_img_format,
                        help=f'Output image format (default: {DXF2IMG.default_img_format})')
    parser.add_argument('--img-res', type=int, default=DXF2IMG.default_img_res,
                        help=f'Output image resolution in DPI (default: {DXF2IMG.default_img_res})')
    args = parser.parse_args()

    # Find all DXF files in the specified directory
    dxf_dir = args.dxf_dir
    dxf_files = glob.glob(os.path.join(dxf_dir, '*.dxf'))

    # Convert DXF files to PNG
    dxf2img = DXF2IMG(img_format=args.img_format, img_res=args.img_res)
    dxf2img.convert_dxf2img(dxf_files)

if __name__ == '__main__':
    main()
