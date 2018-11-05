import math
from tkinter import *
from IdealFlowCalculator import IdealFlowCalculator
from PlotCanvas import PlotCanvas
from ColorScale import ColorScale
import numpy as np

from StreamElementCollection import StreamElementCollection


class IdealFlowSandbox:
    def __init__(self, master):
        self.master = master
        self.current_mode = self.modes["streamline"]
        self.object_counter = 0
        self.init_button_bar()
        self.info_bar = self.init_info_bar()
        self.plot_canvas = self.init_plot()
        self.coords_label = self.init_coords()
        self.StreamElements = StreamElementCollection(self.plot_canvas, self.watcher)

        self.calculator = IdealFlowCalculator(self.plot_canvas.get_scale(), self.StreamElements)

    modes = {
        "streamline": 1,
        "source": 2
    }

    def watcher(self):
        self.clear_streamlines()

    def demo_1(self):
        self.reset()

        self.add_source("Source", 1, 0, 1)
        self.add_source("Sink", -1, 0, -1)

        self.draw_streamlines_around_source(self.StreamElements.get_source("Source"))
        self.redraw()

    def is_mode(self, test):
        return self.current_mode == self.modes[test]

    def set_mode(self, new):
        self.current_mode = self.modes[new]

    def init_coords(self):
        coords_label = Label(self.master)
        coords_label.pack()

        return coords_label

    def init_button_bar(self):
        f = Frame(self.master,
                  borderwidth=1,
                  highlightbackground="Black",
                  height=400)
        f.configure(background="Blue")
        f.pack(side="left", fill="both", expand=True)

        button1 = Button(f, text="Clear Streamlines", command=self.clear_streamlines)
        button1.pack()

        button1 = Button(f, text="Add Source", command=self.toggle_add_source)
        button1.pack()

        button1 = Button(f, text="Add Free Stream", command=self.add_free_stream)
        button1.pack()

        button1 = Button(f, text="New Flow", command=self.reset)
        button1.pack()

        button1 = Button(f, text="Auto Draw", command=self.auto_draw)
        button1.pack()

        button1 = Button(f, text="Demo", command=self.demo_1)
        button1.pack()

    def auto_draw(self):
        for s in self.StreamElements.get_all_sources():
            if s.m > 0:
                self.draw_streamlines_around_source(s)
        self.redraw()

    def reset(self):
        for s in self.StreamElements.get_all_sources():
            s.erase()
        self.StreamElements = StreamElementCollection(self.plot_canvas, self.watcher)
        self.calculator = IdealFlowCalculator(self.plot_canvas.get_scale(), self.StreamElements)
        self.clear_streamlines()
        self.object_counter = 0

    def toggle_add_source(self):
        self.set_mode("source")
        self.StreamElements.add_source("temp", 1, 0, 0)

    def init_info_bar(self):
        info_bar = Frame(self.master,
                         borderwidth=1,
                         highlightbackground="Black",
                         height=400)
        info_bar.configure(background="White")
        info_bar.pack(side="right", fill="both", expand=True)

        return info_bar

    def clear_streamlines(self):
        self.plot_canvas.remove("streamlines")

    def init_plot(self):
        plot_canvas = PlotCanvas(self.master, 400, 800)
        plot_canvas.bind('<Motion>', self.motion)
        plot_canvas.bind('<Button-1>', self.click)

        return plot_canvas

    def add_source(self, tag, m, x, y):
        self.StreamElements.add_source(tag, m, x, y)\
            .control(self.info_bar, self.object_counter)

        self.object_counter += 1
        self.clear_streamlines()

    def add_free_stream(self):
        self.set_mode("streamline")
        self.StreamElements.add_free_stream(1, 0)
        self.clear_streamlines()

    def redraw(self):
        for s in self.StreamElements.get_all_sources():
            s.front()

    def motion(self, event):
        r = self.plot_canvas.cursor_coords(event)
        self.coords_label.config(text='({}, {})'.format(r[0], r[1]))

        if self.is_mode("source"):
            x, y = self.plot_canvas.transform([event.x, event.y])
            self.StreamElements.get_source("temp").move(x, y)

    def click(self, event):
        if self.is_mode("source"):
            self.StreamElements.delete_source("temp")
            self.set_mode("streamline")
            x, y = self.plot_canvas.transform([event.x, event.y])
            self.add_source("Source " + str(self.object_counter + 1), 1, x, y)
        else:
            r = self.plot_canvas.transform([event.x, event.y])
            self.draw_streamline(r)
            self.redraw()

    def draw_streamlines_around_source(self, source):
        for i in np.linspace(0, 2 * math.pi, 31):
            x = source.x + math.cos(i) / 10
            y = source.y + math.sin(i) / 10
            self.draw_streamline([x, y])

    def draw_streamline(self, r):
        points = self.calculator.get_streamline(r)

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            scaled_color = ColorScale.scale_to_color(p1[2], 0, .4)
            self.plot_canvas.draw_line("streamlines",
                                       p1[0], p1[1], p2[0], p2[1],
                                       color=scaled_color,
                                       width=1)
