# Minivan-Plate-Config
An online Minivan plate configurator, hosted at http://MiniVanPlate.xyz/

This is a static site, all plate files and previews are pre-baked, meaning no computation is required on the server or client.

Plate source files are either manually scraped into ```/wiki_scrape``` from https://trashman.wiki/files/, or generated and saved to ```/cutouts``` using a combination of http://www.keyboard-layout-editor.com/, https://plate.keeb.io/, and http://builder.swillkb.com/.

Plate source files from ```/wiki_srape``` and ```/cutouts``` are combined manually using Fusion360, then saved into ```all_dxf```

Plate previews are generated using https://github.com/Hamza442004/DXF2img, and saved under that same filename into ```all_preview```
