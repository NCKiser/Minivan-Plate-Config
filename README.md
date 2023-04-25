# Minivan-Plate-Config
An online Minivan plate configurator, hosted at http://MiniVanPlate.xyz/

This is a static site, all plate files and previews are pre-baked, meaning no computation is required on the server or client.

Plate source files are either manually scraped into ```/wiki_scrape``` from https://trashman.wiki/files/, or generated and saved to ```/cutouts``` using a combination of http://www.keyboard-layout-editor.com/, https://plate.keeb.io/, and http://builder.swillkb.com/.

Plate source files from ```/wiki_srape``` and ```/cutouts``` are combined manually using Fusion360, then saved into ```all_dxf```

Plate previews are generated using https://github.com/Hamza442004/DXF2img, and saved under that same filename into ```all_preview```


## How to make more layouts

Open the ```/utils/All_Plates.f3d``` file in Fusion360

Take the timeline marker to just before the last extrude.

![image](https://user-images.githubusercontent.com/37519411/234330245-4acf69e6-d05e-480c-8d20-735802c6b08e.png)

Insert your switch cutouts .dxf

![image](https://user-images.githubusercontent.com/37519411/234330641-ca5ecb78-c07a-4b70-9f2f-e1254d38a9bc.png)

Select the XZ Plane, and position the the .dxf such that the top-left switch (in 19.05mm spacing) is (or would be) centered on the Origin (or locate in a similar way).

Use the midpoint of the diagonal of the switch cutout to point-to-point move the sketch to the origin.

![image](https://user-images.githubusercontent.com/37519411/234331591-6e3db14f-15bf-435a-988d-fd1a209b63f1.png)

Select all elements in your cutouts sketch and Fix (Lock) them into place.

![image](https://user-images.githubusercontent.com/37519411/234331943-fc5f360e-9737-483c-a64b-44259aa8516c.png)

Finish sketch, progress the timeline forward, and edit the extrude.

![image](https://user-images.githubusercontent.com/37519411/234332169-00e8405b-a969-4bca-8465-eff4632eebea.png)

Unselect any profiles that are selected. Hide the Bodies group. Select the switch cutouts that correspond to your new layout.

![image](https://user-images.githubusercontent.com/37519411/234332432-209c2981-8004-4bbf-92af-b27b186170e0.png)

Un-hide the Bodies group, and OK the Edit Extrude window.

![image](https://user-images.githubusercontent.com/37519411/234332739-1f20bb9a-14f5-4561-baf9-40d3af6c56b7.png)

Progress the timeline marker forward, and ```plate_campiander```, ```plate_campsite```, ```plate_coriander```, ```plate_hull```, and ```plate_tray``` should be generated.

![image](https://user-images.githubusercontent.com/37519411/234333385-8903c44e-be9a-41ac-9b2c-8ac7ad42c2b0.png)

Right-click on those 5 sketches and save them as .dxf using a unique filename into ```/all_dxf```

![image](https://user-images.githubusercontent.com/37519411/234333590-a7c08883-efc6-44b1-84b1-c6da0dc9cdd4.png)

![image](https://user-images.githubusercontent.com/37519411/234333806-1b5acd96-58ff-4ef1-8fc1-5b01e6ede496.png)

Add the layout entry in ```index.html```, being sure the entry's ```value``` is the same as your filename component.

![image](https://user-images.githubusercontent.com/37519411/234334379-3d3b2d23-5876-45b2-aedb-9b6172151f49.png)


