import ezdxf
from PIL import Image

def dxf_to_png(dxf_path, png_path):
    # Load the DXF file using the ezdxf library
    dwg = ezdxf.readfile(dxf_path)
    
    # Get the model space layout
    modelspace = dwg.modelspace()
    
    # Get the extents of the drawing
    extmin = modelspace.extmin
    extmax = modelspace.extmax
    
    # Set the image size based on the drawing extents
    width = int(extmax[0] - extmin[0])
    height = int(extmax[1] - extmin[1])
    
    # Create a new image using the Pillow library
    img = Image.new("RGB", (width, height), "white")
    
    # Draw the DXF entities onto the image
    for entity in modelspace:
        if entity.dxftype() == "LINE":
            start = (entity.dxf.start[0] - extmin[0], entity.dxf.start[1] - extmin[1])
            end = (entity.dxf.end[0] - extmin[0], entity.dxf.end[1] - extmin[1])
            imgdraw = ImageDraw.Draw(img)
            imgdraw.line([start, end], fill="black", width=1)
    
    # Save the image as a PNG file
    img.save(png_path)
