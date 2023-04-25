import ezdxf
import os

def convert_dxf_to_png(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()
    ext = msp.extmax
    doc.set_modelspace_vport(0, ext)
    doc.saveas(output_file)

if not os.path.exists('all_preview'):
    os.makedirs('all_preview')

for file in os.listdir('all_dxf'):
    if file.endswith('.dxf'):
        filename = os.path.splitext(file)[0]
        dxf_file = os.path.join('all_dxf', file)
        png_file = os.path.join('all_preview', f'{filename}.png')
        if os.path.exists(png_file):
            print(f'File {png_file} already exists, skipping.')
        else:
            print(f'Converting {dxf_file} to {png_file}')
            convert_dxf_to_png(dxf_file, png_file)
