# cratelight_gui
This is a GUI aimed to streamline creation of graphics and animations for [CrateLight](https://github.com/fablabnk/CrateLight) project of [FabLab NK](https://github.com/fablabnk). Current version only functions in a pixel-art mode, but is easy to adjust for image loading.

This script should work out of the box with any python3.10+ installation, as the only package it uses is vanilla Tkinter, that is a part of the standard python library.
As this is the my first use of Tkinter, some of the elements might be too heavy for the purpose I've used them. Thus, each pixel is basically a button that changes it's color and the underlying array element according to user preferences. A Wall of 32x32 pixels results in ~1000 buttons, which makes the app renderer to struggle noticeably.

# Usage

```
python3 app.py
```

1. On the initial tab user must specify dimensions of the crate (number of LEDs) and the wall (number of crates), as well as crate layout (ie direction of wiring from the first to the last LED, as if they look at the front side of the crate):

![Layout 1](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout1.png)
![Layout 2](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout2.png)
![Layout 3](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout3.png)
![Layout 4](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout4.png)
![Layout 5](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout5.png)
![Layout 6](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout6.png)
![Layout 7](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout7.png)
![Layout 8](https://github.com/k-off/cratelight_gui/blob/master/assets/Layout8.png)

Wall dimensions are the max width and height of the entire installation, as the app allows user to arrange crates in arbitrary order and shape.
App also allows creation of multiple Walls, that might help to circumvent possible limitations of LED strip length and/or to increase framerate by splitting of an image into several chunks (walls). 

![Wall and Crate Settings](https://github.com/k-off/cratelight_gui/blob/master/pics/00.png)

2. After pressing `Create New Wall` button a new Tab will appear. There user must index crates in direction of wiring from the first to the last crate, as if they look at the front side of the wall. Indexing option is in the context menu (right click on each of the crates). Indexing must not be sequenial, ie 1,3,5 is allowed in range 0..wall_width*wall_height. There is no protection against index duplicates, though, so user has to enter them with caution. If user decides that a crate should be excluded from the wall (disabled), they should set index of that crate to -1. In this case relaxed indexing allows to avoid reindexing of the crates that are after the disabled one.

One can also add and remove an extra LED between crates by ckecking or unchecking the corresponding option in the context menu for each crate (extra LED is enabled for all crates by default).
It is also possible to set up the layout of each crate individually (by default all crates have the same layout as set by user on the initial tab of the app).

![Wall 0 context menu](https://github.com/k-off/cratelight_gui/blob/master/pics/01.png)

3. User can spawn color palette by clicking the `Select color` button and then choose the color of their preference. After selecting the color they should click on every Pixel on the wall, that is supposed to store this color.

![Wall 0 color palette](https://github.com/k-off/cratelight_gui/blob/master/pics/02.png)

4. After setting up the Wall, user might press the `Save` button to store current state in the `.crate` file, that could be directly fed to the Raspbery Py

# TODO

 - add `Send` feature to send the entire frame directly to the Raspberry Pi 
 - add interactive mode (click on the pixel in GUI app should result in an immediate Wall update)
 - add `Save` and `Load` features to re/store application state for later use
 - add `Import` feature to load images, GIFs (and videos?)
 - do all of the above for multiple Walls at the same time
   
