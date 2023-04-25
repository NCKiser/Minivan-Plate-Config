import os
import sys
import ezdxf
from PIL import Image, ImageDraw

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <input directory> <output directory>")
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.isdir(input_dir):
    print(f"{input_dir} is not a directory")
    sys.exit(1)

if not os.path.isdir(output_dir):
    print(f"{output_dir} is not a directory")
    sys.exit(1)

for dxf_file in os.listdir(input_dir):
    if not dxf_file.endswith('.dxf'):
        continue
    
    png_file = os.path.join(output_dir, os.path.splitext(dxf_file)[0] + '.png')

    if os.path.isfile(png_file):
        print(f"{png_file} already exists, skipping...")
        continue

    dxf_path = os.path.join(input_dir, dxf_file)
    print(f"Converting {dxf_path} to {png_file}")

    try:
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        bbox = msp.bounding_box()
        ext = (bbox[0], bbox[1])
        width, height = int(abs(ext[0][0]-ext[1][0])), int(abs(ext[0][1]-ext[1][1]))
        img = Image.new('RGB', (width, height), color='white')
        img_draw = ImageDraw.Draw(img)
        for entity in msp:
            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                img_draw.line([(start[0]-ext[0][0], height - (start[1]-ext[0][1])), 
                                (end[0]-ext[0][0], height - (end[1]-ext[0][1]))], 
                                fill='black', width=1)
            elif entity.dxftype() == 'LWPOLYLINE':
                for i in range(len(entity)):
                    start = entity[i - 1].dxf.end
                    end = entity[i].dxf.end
                    img_draw.line([(start[0]-ext[0][0], height - (start[1]-ext[0][1])), 
                                    (end[0]-ext[0][0], height - (end[1]-ext[0][1]))], 
                                    fill='black', width=1)
        img.save(png_file)
    except ezdxf.DXFStructureError:
        print(f"{dxf_path} is an invalid DXF file")
    except Exception as e:
        print(f"Error converting {dxf_path} to {png_file}: {str(e)}")
