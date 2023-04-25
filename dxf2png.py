import ezdxf
import argparse
import os

def convert_dxf_to_png(input_file, output_file):
    dxf = ezdxf.readfile(input_file)
    modelspace = dxf.modelspace()

    # Get bounding box
    x_min, y_min, _, _ = modelspace.get_bbox()
    _, _, x_max, y_max = modelspace.get_bbox()

    # Set up image size
    width = int((x_max - x_min) * SCALE_FACTOR)
    height = int((y_max - y_min) * SCALE_FACTOR)

    # Create the image
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw the entities in the drawing
    for entity in modelspace:
        if entity.dxftype() == "LINE":
            start = entity.dxf.start
            end = entity.dxf.end
            draw.line(
                (
                    (start[0] - x_min) * SCALE_FACTOR,
                    height - (start[1] - y_min) * SCALE_FACTOR,
                    (end[0] - x_min) * SCALE_FACTOR,
                    height - (end[1] - y_min) * SCALE_FACTOR,
                ),
                fill=COLOR,
                width=LINE_WIDTH,
            )
        elif entity.dxftype() == "LWPOLYLINE":
            polyline = entity.get_points("xy")
            for i in range(len(polyline) - 1):
                start = polyline[i]
                end = polyline[i + 1]
                draw.line(
                    (
                        (start[0] - x_min) * SCALE_FACTOR,
                        height - (start[1] - y_min) * SCALE_FACTOR,
                        (end[0] - x_min) * SCALE_FACTOR,
                        height - (end[1] - y_min) * SCALE_FACTOR,
                    ),
                    fill=COLOR,
                    width=LINE_WIDTH,
                )

    # Save the image
    image.save(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to input DXF file')
    parser.add_argument('output_file', help='path to output PNG file')
    args = parser.parse_args()

    convert_dxf_to_png(args.input_file, args.output_file)
