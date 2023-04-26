import os
import re
import argparse
import logging
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

logging.basicConfig(level=logging.INFO)


class DXF2IMG(object):

    def __init__(self, img_format, img_res):
        self.img_format = img_format
        self.img_res = img_res

    def convert_dxf2img(self, dxf_path, preview_path):
        logging.info(f"Converting DXF files in {dxf_path} to {self.img_format.upper()} at {self.img_res} DPI")
        if not os.path.exists(dxf_path):
            logging.error(f"{dxf_path} does not exist!")
            return

        if not os.path.isdir(dxf_path):
            logging.error(f"{dxf_path} is not a directory!")
            return

        os.makedirs(preview_path, exist_ok=True)

        for filename in os.listdir(dxf_path):
            dxf_file = os.path.join(dxf_path, filename)

            if not dxf_file.lower().endswith(".dxf"):
                logging.warning(f"{dxf_file} is not a DXF file, skipping")
                continue

            img_file = os.path.join(preview_path, os.path.splitext(filename)[0] + self.img_format)

            if os.path.exists(img_file):
                logging.warning(f"{img_file} already exists, skipping")
                continue

            try:
                doc = ezdxf.readfile(dxf_file)
                msp = doc.modelspace()
                # Recommended: audit & repair DXF document before rendering
                auditor = doc.audit()
                # The auditor.errors attribute stores severe errors,
                # which *may* raise exceptions when rendering.
                if len(auditor.errors) != 0:
                    logging.error(f"{dxf_file} is damaged and can't be converted!")
                else:
                    fig = plt.figure()
                    ax = fig.add_axes([0, 0, 1, 1])
                    ctx = RenderContext(doc)
                    ctx.set_current_layout(msp)
                    # ctx.current_layout.set_colors(bg='#FFFFFF')
                    out = MatplotlibBackend(ax)
                    Frontend(ctx, out).draw_layout(msp, finalize=True)

                    fig.savefig(img_file, dpi=self.img_res)
                    logging.info(f"Converted {dxf_file} to {img_file[:-3]}")
            except Exception as e:
                logging.error(f"Error converting {dxf_file}: {e}")

        logging.info("Conversion complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert DXF files to PNG')
    parser.add_argument('dxf_dir', help='Directory containing DXF files')
    parser.add_argument('--img-format', default='.png', help='Output image format (default: .png)')
    parser.add_argument('--img-res', type=int, default=300, help='Output image resolution (default: 300)')
    args = parser.parse_args()

    converter = DXF2IMG(args.img_format, args.img_res)
    converter.convert_dxf2img(args.dxf_dir, os.path.join(os.getcwd(), 'all_preview'))
