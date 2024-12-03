# cratelight_gui
This is a GUI aimed to streamline creation of graphics and animations for [CrateLight](https://github.com/fablabnk/CrateLight) project of [FabLab NK](https://github.com/fablabnk). Current version only functions in a pixel-art mode, but is easy to adjust for image loading.

This script should work out of the box with any python3.10+ installation, as the only package it uses is vanilla Tkinter, that is a part of the standard python library.
As this is the my first use of Tkinter, some of the elements might be too heavy for the purpose I've used them. Thus, each pixel is basically a button that changes it's color and the underlying array element according to user preferences. A Wall of 32x32 pixels results in a ~1000 buttons, which makes the app renderer to struggle noticeably.

# Usage

```
python3 app.py
```

1. On the initial tab user must specify crate- (number of LEDs) and wall- (number of crates) dimensions, as well as crate layout (ie direction of wiring from the first to the last LED, as if they look at the front side of the crate):

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

2. After pressing `Create New Wall` button a new Tab will appear. There user must index crates in direction of wiring from the first to the last crate, as if they look at the front side of the wall. Indexing option is in the context menu (right click on each of the crates).
