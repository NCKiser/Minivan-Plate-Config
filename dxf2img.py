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
            file_path = name
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise exception("The DXF document is damaged and can't be converted!")
            else :
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)  # Use set_current_layout instead
                ctx.set_current_layout.set_colors(bg='#FFFFFF')  # No need to set colors on the current_layout
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                img_name = re.findall("(\S+)\.",os.path.basename(name))  # select the image name that is the same as the dxf file name
                first_param = ''.join(img_name) + self.img_format  #concatenate list and string
                fig.savefig(os.path.join('all_preview', first_param), dpi=self.img_res)  # Save to 'all_preview' folder



if __name__ == '__main__':
    dxf_folder = 'all_dxf'
    img_folder = 'all_preview'

    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    converter = DXF2IMG()
    for dxf_file in glob.glob(os.path.join(dxf_folder, '*.dxf')):
        converter.convert_dxf2img([dxf_file])
        print(f'{dxf_file} converted to an image')

        # move the converted image to the preview folder
        img_name = re.findall("(\S+)\.", os.path.basename(dxf_file))[0] + converter.img_format
        img_path = os.path.join(img_folder, img_name)
        shutil.move(os.path.join(dxf_folder, img_name), img_path)
        print(f'{img_name} moved to {img_path}')
