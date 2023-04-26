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
        
        dxf_pattern = re.compile(r".+\.dxf$", re.IGNORECASE)
        for filename in os.listdir(dxf_path):
            if not dxf_pattern.match(filename):
                logging.warning(f"{filename} is not a DXF file, skipping")
                continue
            
            dxf_file = os.path.join(dxf_path, filename)
            img_file = os.path.join(preview_path, os.path.splitext(filename)[0] + "." + self.img_format)
            
            if os.path.isfile(img_file):
                logging.warning(f"{img_file} already exists, skipping")
                continue
            
            if not os.path.isfile(dxf_file):
                logging.warning(f"{dxf_file} does not exist, skipping")
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
                    logging.info(f"Converted {dxf_file} to {img_file}")
            except Exception as e:
                logging.error(f"Error converting {dxf_file}: {e}")
        
        logging.info("Conversion complete")
