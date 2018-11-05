import math
from tkinter import *


class Source:
    def __init__(self, master, tag, m, x, y):
        self.m = m
        self.x = x
        self.y = y
        self.display = tag
        self.tag = str.replace(tag, " ", "")
        self.master = master
        self.border_frame = None

        self.edit_mode = False

    def u(self, x, y):
        factor = self.m / (2 * math.pi)
        num = x - self.x
        den = math.pow(x - self.x, 2) + math.pow(y - self.y, 2)
        return factor * num / den

    def v(self, x, y):
        factor = self.m / (2 * math.pi)
        num = y - self.y
        den = math.pow(x - self.x, 2) + math.pow(y - self.y, 2)
        return factor * num / den

    def draw(self):
        self.master.draw_circle(self.tag, self.x, self.y, "Green", radius=0.1)
        size = .05
        self.master.draw_line(self.tag, self.x - size, self.y, self.x + size, self.y, "White")
        if self.m > 0:
            self.master.draw_line(self.tag, self.x, self.y - size + .01, self.x, self.y + size + .01, "White")

    def erase(self):
        self.master.remove(self.tag)
        if self.border_frame:
            self.border_frame.destroy()

    def front(self):
        self.master.tag_raise(self.tag)

    def move(self, x, y):
        self.master.move(self.tag, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def control(self, master, row):
        if row % 2 == 0:
            color = "White"
        else:
            color = "LightGrey"

        self.border_frame = Frame(master,
                                  borderwidth=1,
                                  highlightbackground="Black")
        self.border_frame.configure(background="Black")
        self.border_frame.pack()

        container_frame = Frame(self.border_frame)
        container_frame.configure(background=color)
        container_frame.pack()

        s = self.display + '\n'
        s += "m: " + str(self.m) + '\n'
        s += "p: (" + str(self.x) + ", " + str(self.y) + ")"

        title = Label(container_frame, text=s, bg=color, justify="left", width=12)
        title.bind("<Button-1>", self.toggle_edit)
        title.pack()

        self.edit_frame = Frame(container_frame)
        self.edit_frame.configure(background=color)
        self.edit_frame.pack()

        self.create_edit_field("m:", color, str(self.m), 1)
        self.create_edit_field("x:", color, str(self.x), 2)
        self.create_edit_field("y:", color, str(self.y), 3)

        self.toggle_edit(None)

        return self.edit_frame

    def create_edit_field(self, var, color, default, row):
        label = Label(self.edit_frame, text=var, bg=color)
        label.grid(row=row, column=0, sticky="E")
        entry = Entry(self.edit_frame, width=9)
        entry.insert(END, default)
        entry.grid(row=row, column=1, sticky="W")

    def toggle_edit(self, event):
        if not self.edit_mode:
            self.edit_frame.pack_forget()
            self.edit_mode = True
        else:
            self.edit_frame.pack()
            self.edit_mode = False
