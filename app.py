"""
MIT License

Copyright (c) 2024 k-off

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import Menu, Event
from tkinter import simpledialog

from sys import platform
if platform == "linux" or platform == "linux2" or platform == "win32":
    from tkinter import Button # TODO: test on these platforms
    borderless_option = {}
elif platform == "darwin":
    from tkmacosx import Button # allows to change color of buttons on macos
    borderless_option = {"borderless": 1}


def validate_positive_int(value: str, label: tk.Label) -> bool:
    try:
        if value is None or len(value) < 1:
            label.config(text="Empty  ", foreground="orange")
            return False
        if int(value) > 0:
            label.config(text="Valid  ", foreground="green")
            return True
        else:

            label.config(text="Invalid", foreground="red")
            return False
    except:
        label.config(text="Invalid", foreground="red")
        return False

def get_scrollable_frame(master, w: int, h: int) -> tuple[ttk.Frame, ttk.Frame]:
    # create contaner-frame, canvas and scrollbars
    containing_frame = ttk.Frame(master)
    canvas = tk.Canvas(containing_frame)
    scrollbar_v = ttk.Scrollbar(containing_frame, orient="vertical", command=canvas.yview)
    scrollbar_h = ttk.Scrollbar(containing_frame, orient="horizontal", command=canvas.xview)

    # set up scrollable frame
    scrollable_frame = ttk.Frame(canvas, width=w, height=h, borderwidth=1, relief="solid")
    scrollable_frame.bind( "<Configure>", lambda e: canvas.configure( scrollregion=canvas.bbox("all") ) )

    # configure canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_v.set)
    canvas.configure(xscrollcommand=scrollbar_h.set)

    # pack 
    scrollbar_h.pack(side="bottom", fill="x")
    scrollbar_v.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    return containing_frame, scrollable_frame

class Wall:
    def __init__(self, name:str, container:tk.Frame, content:tk.Frame, width:int, height:int, crate_width:int, crate_height:int, crate_layout:str) -> None:
        self.name = name
        self.container = container
        self.content = content
        self.width = width
        self.height = height
        self.crate_height = crate_height
        self.crate_width = crate_width
        self.crate_layout = crate_layout
        
        self.palette = tk.Frame(self.container, width=50, height=100, borderwidth=1, relief="solid")
        self.current_color = [((128, 0, 128), "#52b4d8")]
        self.color_button = Button(self.palette, text="Select Color", command=self.select_color, bg=self.current_color[0][-1], **borderless_option)
        self.color_button.pack()

        self.save_button = Button(self.palette, text="Save", command=self.save, bg="white", **borderless_option)
        self.save_button.pack()

        self.crates = []

        self.palette.pack(side="left")
        for x in range(self.width):
            for y in range(self.height):
                self.crates.append(Crate(self.content, self.crate_width, self.crate_height, self.crate_layout, self.current_color, y, x, self.width * self.height))

    def select_color(self):
        self.current_color[0] = colorchooser.askcolor(title ="Palette")
        self.color_button.configure(bg=self.current_color[0][-1])
        # for crate in self.crates:
        #     print(crate.color_grid)

    def save(self):
        output = b""
        for crate in sorted(self.crates):
            if crate.idx < 0:
                continue
            for color in crate.color_grid:
                output += bytes(color[0])
        with open(f"./{self.name}_w{self.width}_h{self.height}_cw{self.crate_width}_ch{self.crate_height}.crate", "wb+") as f:
            print(output)
            f.write(output)

    def __del__(self) -> None:
        self.container.destroy()

class Crate:
    def __init__(self, parent, width:int, height:int, layout:str, current_color:tuple, row:int, col:int, max_index:int, extra_pixel=0) -> None:
        self.width = width
        self.height = height
        self.layout = layout
        self.current_color = current_color
        self.row = row
        self.col = col
        self.idx = -1 # TODO: let user set index of the crate in the chain of crates
        self.body = tk.Frame(parent, width=40, height=30, borderwidth=1, relief="solid", bg="#ffffff")
        self.body.grid(row=row, column=col, padx=1, pady=1)
        self.extra_pixel = tk.IntVar(value=1)
        self.max_index = max_index
        self.color_grid = list(((0, 0, 0), "#000000") for x in range(height * width + self.extra_pixel.get())) # stored values that shall be sent to the arduino after preps
        self.pixel_grid = []                                                                                         # representation of stored values in this app
        for y in range(self.height):
            for x in range(self.width):
                self.pixel_grid.append(Pixel(self.body, 10, 10, self.current_color, self.color_grid, y, x))
        self.change_layout(self.layout)

        def manage_extra_pixel():
            if self.extra_pixel.get():
                self.color_grid.append(((0, 0, 0), "#000000"))
            else:
                self.color_grid.pop()

        # add context menu
        menu = Menu(self.body, tearoff=0)
        menu.add_checkbutton(label="Extra pixel", variable=self.extra_pixel, command=manage_extra_pixel)
        menu.add_separator()
        menu.add_command(label=f"Set Index (current {self.idx})", command=lambda: self.set_index(menu))
        menu.add_separator()
        menu.add_command(label="Layout1", command=lambda: self.change_layout("Layout1"))
        menu.add_command(label="Layout2", command=lambda: self.change_layout("Layout2"))
        menu.add_command(label="Layout3", command=lambda: self.change_layout("Layout3"))
        menu.add_command(label="Layout4", command=lambda: self.change_layout("Layout3"))
        menu.add_command(label="Layout5", command=lambda: self.change_layout("Layout5"))
        menu.add_command(label="Layout6", command=lambda: self.change_layout("Layout6"))
        menu.add_command(label="Layout7", command=lambda: self.change_layout("Layout7"))
        menu.add_command(label="Layout8", command=lambda: self.change_layout("Layout8"))

        def do_popup(event:Event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        self.body.bind("<Button-2>" if platform == "darwin" else "<Button-3>", do_popup) # TODO: test on these platforms

    def set_index(self, menu:Menu):
        idx = simpledialog.askinteger(title="Crate index in the chain of crates", prompt="Type current crate index (-1 to exclude from the chain): ", minvalue=-1, maxvalue=self.max_index)
        if not idx is None:
            self.idx = idx
        if (self.idx < 0):
            for pixel in self.pixel_grid:
                pixel.button.configure(state="disabled")
        else:
            for pixel in self.pixel_grid:
                pixel.button.configure(state="normal")
        menu.entryconfigure(2, label=f"Set Index (current {self.idx})")

    def change_layout(self, layout:str):
        # print(f"changing layout from {self.layout} to {layout}")
        self.layout = layout
        idx = 0
        even = True
        match self.layout:
            case "Layout1":                                     # horisontal (V)
                for y in range(self.height-1, -1, -1):          # bottom->top
                    if even:
                        for x in range(0, self.width, 1):       # left->right
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for x in range(self.width-1, -1, -1):   # right->left
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout2":                                     # horisontal (V)
                for y in range(0, self.height, 1):              # top->bottom
                    if even:
                        for x in range(0, self.width, 1):       # left->right
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for x in range(self.width-1, -1, -1):   # right->left
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout3":                                     # horisontal (V)
                for y in range(0, self.height, 1):              # top->bottom
                    if not even:
                        for x in range(0, self.width, 1):       # left->right
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for x in range(self.width-1, -1, -1):   # right->left
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout4":                                     # horisontal (V)
                for y in range(self.height-1, -1, -1):          # bottom->top
                    if not even:
                        for x in range(0, self.width, 1):       # left->right
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for x in range(self.width-1, -1, -1):   # right->left
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout5":                                     # vertical (V)
                for x in range(0, self.width, 1):               # left->right
                    if even:
                        for y in range(self.height-1, -1, -1):  # bottom->top
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for y in range(self.height):            # top->bottom
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout6":                                     # vertical (V)
                for x in range(0, self.width, 1):               # left->right
                    if not even:
                        for y in range(self.height-1, -1, -1):  # bottom->top
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for y in range(self.height):            # top->bottom
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout7":                                     # vertical (V)
                for x in range(self.width-1, -1, -1):           # right->left
                    if not even:
                        for y in range(self.height-1, -1, -1):  # bottom->top
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for y in range(self.height):            # top->bottom
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case "Layout8":                                     # vertical (V)
                for x in range(self.width-1, -1, -1):           # right->left
                    if even:
                        for y in range(self.height-1, -1, -1):  # bottom->top
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    else:
                        for y in range(self.height):            # top->bottom
                            self.pixel_grid[x + self.width*y].idx = idx
                            idx += 1
                    even = not even
            case _:
                pass

    def __lt__(self, other):
        return self.idx < other.idx


class Pixel:
    def __init__(self, parent, width:int, height:int, current_color:tuple, saved_color:list, row:int, col:int) -> None:
        self.parent = parent
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.idx = 0 # idx of this pixel in the crate.color_grid, depends on layout
        self.current_color = current_color
        self.saved_color = saved_color
        self.button = Button(self.parent, text="", command=self.save_color, bg="#000000", width=self.width, height=self.height, borderwidth=1, relief="solid", state="disabled")
        self.button.grid(row=row, column=col, pady=2, padx=2)
    
    def save_color(self):
        self.saved_color[self.idx] = self.current_color[0]
        self.button.configure(bg=self.current_color[0][-1])

class App:
    def __init__(self, display_name:str, width:int, height:int) -> None:
        self.root = tk.Tk()
        self.root.title(display_name)
        self.root.geometry(f"{width}x{height}")
        self.root.eval('tk::PlaceWindow . center')
        self.root.focus_force()
        self.walls = []

        # create main tab
        self.window_tabs = ttk.Notebook(self.root)
        self.window_tabs.pack(expand=True, fill="both")
        self.main_tab_container, self.main_tab_content = get_scrollable_frame(self.window_tabs, width, height)
        self.setup_main_page(self.main_tab_content)
        self.window_tabs.add(self.main_tab_container, text=f"Wall and Crate Settings")

        self.root.mainloop()

    def setup_main_page(self, parent: ttk.Frame) -> None:
        # create crate frame contents
        frame_crate_info = ttk.Frame(parent, borderwidth=1, relief="solid")
        lbl_crate = ttk.Label(frame_crate_info, text="Crate Info")

        lbl_crate_width = ttk.Label(frame_crate_info, text="Crate Width", width=10)
        self.lbl_crate_width_valid = ttk.Label(frame_crate_info, text="Empty  ", foreground="orange")
        self.ent_crate_width = ttk.Entry(frame_crate_info, validatecommand=lambda: validate_positive_int(self.ent_crate_width.get(), self.lbl_crate_width_valid), validate="focusout")

        lbl_crate_height = ttk.Label(frame_crate_info, text="Crate Height", width=10)
        self.lbl_crate_height_valid = ttk.Label(frame_crate_info, text="Empty  ", foreground="orange")
        self.ent_crate_height = ttk.Entry(frame_crate_info, validatecommand=lambda: validate_positive_int(self.ent_crate_height.get(), self.lbl_crate_height_valid), validate="focusout")

        self.arr_crate_layouts = ["Layout1", "Layout2", "Layout3", "Layout4", "Layout5", "Layout6", "Layout7", "Layout8"]
        self.str_crate_layout = tk.StringVar(parent)
        self.str_crate_layout.set("Layout1")
        crate_layout_menu = tk.OptionMenu(frame_crate_info, self.str_crate_layout, *self.arr_crate_layouts)

        self.img_crate_layouts = (tk.PhotoImage(file=f"./assets/Layout1.png"),
                tk.PhotoImage(file=f"./assets/Layout2.png"),
                tk.PhotoImage(file=f"./assets/Layout3.png"),
                tk.PhotoImage(file=f"./assets/Layout4.png"),
                tk.PhotoImage(file=f"./assets/Layout5.png"),
                tk.PhotoImage(file=f"./assets/Layout6.png"),
                tk.PhotoImage(file=f"./assets/Layout7.png"),
                tk.PhotoImage(file=f"./assets/Layout8.png"))
        lbl_crate_layout = tk.Label(frame_crate_info, image=self.img_crate_layouts[0], width=64, height=64)
        def change_layout_img(*args):
            lbl_crate_layout.config(image=self.img_crate_layouts[self.arr_crate_layouts.index(self.str_crate_layout.get())])
        self.str_crate_layout.trace_add("write", change_layout_img)

        #pack crate frame
        lbl_crate.grid(row=0, column=0, columnspan=3)
        lbl_crate_width.grid(row=1, column=0, columnspan=1)
        self.ent_crate_width.grid(row=1, column=1, columnspan=1)
        self.lbl_crate_width_valid.grid(row=1, column=2, columnspan=1)
        lbl_crate_height.grid(row=2, column=0, columnspan=1)
        self.ent_crate_height.grid(row=2, column=1, columnspan=1)
        self.lbl_crate_height_valid.grid(row=2, column=2, columnspan=1)
        crate_layout_menu.grid(row=3, column=0, columnspan=1)
        lbl_crate_layout.grid(row=3, column=1, columnspan=2)
        frame_crate_info.grid(row=0, column=0, padx=5, pady=5)

        # create wall frame contents
        frame_wall_info = ttk.Frame(parent, borderwidth=1, relief="solid")
        lbl_wall = ttk.Label(frame_wall_info, text="Wall Info")

        lbl_wall_width = ttk.Label(frame_wall_info, text="Wall Width", width=10)
        self.lbl_wall_width_valid = ttk.Label(frame_wall_info, text="Empty  ", foreground="orange")
        self.ent_wall_width = ttk.Entry(frame_wall_info, validatecommand=lambda: validate_positive_int(self.ent_wall_width.get(), self.lbl_wall_width_valid), validate="focusout")

        lbl_wall_height = ttk.Label(frame_wall_info, text="Wall Height", width=10)
        self.lbl_wall_height_valid = ttk.Label(frame_wall_info, text="Empty  ", foreground="orange")
        self.ent_wall_height = ttk.Entry(frame_wall_info, validatecommand=lambda: validate_positive_int(self.ent_wall_height.get(), self.lbl_wall_height_valid), validate="focusout")

        # pack wall frame
        lbl_wall.grid(row=0, column=0, columnspan=3)
        lbl_wall_width.grid(row=1, column=0, columnspan=1)
        self.ent_wall_width.grid(row=1, column=1, columnspan=1)
        self.lbl_wall_width_valid.grid(row=1, column=2, columnspan=1)
        lbl_wall_height.grid(row=2, column=0, columnspan=1)
        self.ent_wall_height.grid(row=2, column=1, columnspan=1)
        self.lbl_wall_height_valid.grid(row=2, column=2, columnspan=1)
        frame_wall_info.grid(row=1, column=0, padx=5, pady=10)

        button = Button(parent, text="Create New Wall", command=self.add_wall, bg="#00cc00", **borderless_option)
        button.grid(row=4, column=0, columnspan=3)
        
    def add_wall(self) -> None:
        self.root.focus()
        if not self.lbl_wall_height_valid.cget("text") == self.lbl_wall_width_valid.cget("text") == self.lbl_crate_height_valid.cget("text") == self.lbl_wall_width_valid.cget("text") == "Valid  ":
            messagebox.showinfo(message="All Crate and Wall values must be valid")
        else:
            wall_name = f"Wall {len(self.walls)}"
            container, content = get_scrollable_frame(self.window_tabs, 1000, 1000)
            self.walls.append(Wall(wall_name, container, content, int(self.ent_wall_width.get()), int(self.ent_wall_height.get()), int(self.ent_crate_width.get()), int(self.ent_crate_height.get()), self.str_crate_layout.get()))
            self.window_tabs.add(self.walls[-1].container, text=self.walls[-1].name)

if __name__ == "__main__":
    app = App(display_name=" CrateLight GUI", width=450, height=430)
