import os
import re
import glob
import shutil
import ezdxf
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


class DXF2IMG(object):

    def __init__(self, img_format='.png', img_res=300):
        self.img_format = img_format
        self.img_res = img_res

    def convert_dxf2img(self, names):
        for name in names:
            file_path = os.path.join('all_dxf', name)
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise Exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)  # Use set_current_space_layout instead
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                img_name = re.findall("(\S+)\.", name)[0] + self.img_format  # select the image name that is the same as the dxf file name
                img_path = os.path.join('all_preview', img_name)
                fig.savefig(img_path, dpi=self.img_res)  # Save to 'all_preview' folder
                print(f'{name} converted to {img_path}')

if __name__ == '__main__':
    dxf_folder = 'all_dxf'
    img_folder = 'all_preview'

    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    converter = DXF2IMG()
    for dxf_file in glob.glob(os.path.join(dxf_folder, '*.dxf')):
        filename = os.path.basename(dxf_file)
        converter.convert_dxf2img([filename])
        print(f'{filename} converted to an image')

        # move the converted image to the preview folder
        img_name = re.findall("(\S+)\.", filename)[0] + converter.img_format
        img_path = os.path.join(img_folder, img_name)
        shutil.move(os.path.join('all_preview', img_name), img_path)
        print(f'{img_name} moved to {img_path}')
