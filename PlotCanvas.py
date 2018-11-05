from tkinter import Canvas, Frame


class PlotCanvas:
    def __init__(self, master, height, width):
        self.__PLOT_WIDTH = width
        self.__PLOT_HEIGHT = height
        self.__master = master
        master.title("2D Ideal Flow Sandbox")
        self.__gap_x = 50
        self.__gap_y = 50
        self.__plot = self.__create_plot()

    def bind(self, trigger, event):
        self.__plot.bind(trigger, event)

    def cursor_coords(self, event):
        x = self.__transform_x_inverse(event.x)
        y = self.__transform_y_inverse(event.y)

        return [x, y]

    # Initialize __plot canvas
    def __create_plot(self):
        # Create Border
        plot_frame = Frame(self.__master,
                           borderwidth=1,
                           highlightbackground="Black")
        plot_frame.configure(background="Black")

        # Create Canvas
        plot = Canvas(plot_frame,
                      width=self.__PLOT_WIDTH,
                      height=self.__PLOT_HEIGHT,
                      background="White")

        # Draw Axes
        middle_x = self.__PLOT_WIDTH / 2
        middle_y = self.__PLOT_HEIGHT / 2
        plot.create_line(middle_x, 0, middle_x, self.__PLOT_HEIGHT, fill="Black", width=3)
        plot.create_line(0, middle_y, self.__PLOT_WIDTH, middle_y, fill="Black", width=3)

        # Draw Grid Points
        for center_x in range(self.__gap_x, self.__PLOT_WIDTH, self.__gap_x):
            for center_y in range(self.__gap_y, self.__PLOT_HEIGHT, self.__gap_y):
                size = 3
                plot.create_line(center_x, center_y - size, center_x, center_y + size + 1, fill="Black", width=1)
                plot.create_line(center_x - size, center_y, center_x + size + 1, center_y, fill="Black", width=1)

        # Finish Plot Creation
        plot.pack()
        plot_frame.pack()
        return plot

    def draw_circle(self, tag, center_x, center_y, color="Red", radius=1, border=""):
        center_x = self.__transform_x(center_x)
        center_y = self.__transform_y(center_y)

        return self.__plot.create_oval(center_x - radius * self.__gap_x,
                                       center_y - radius * self.__gap_y,
                                       center_x + radius * self.__gap_x,
                                       center_y + radius * self.__gap_y,
                                       fill=color,
                                       outline=border,
                                       tag=tag)

    def draw_line(self, tag, start_x, start_y, end_x, end_y, color="Black", width=1):
        start_x = self.__transform_x(start_x)
        end_x = self.__transform_x(end_x)
        start_y = self.__transform_y(start_y)
        end_y = self.__transform_y(end_y)

        return self.__plot.create_line(start_x,
                                       start_y,
                                       end_x,
                                       end_y,
                                       fill=color,
                                       width=width,
                                       tag=tag)

    def move(self, tag, x, y):
        x = self.__transform_x(0) - self.__transform_x(x)
        y = self.__transform_y(0) - self.__transform_y(y)
        self.__plot.move(tag, -x, -y)

    def remove(self, tag):
        self.__plot.delete(tag)

    def tag_raise(self, tag):
        self.__plot.tag_raise(tag)

    def get_scale(self):
        return (self.__gap_x + self.__gap_y) / 2

    def transform(self, r):
        return [self.__transform_x_inverse(r[0]), self.__transform_y_inverse(r[1])]

    def plot_width(self):
        return self.__PLOT_WIDTH / self.__gap_x / 2

    def __transform_x(self, x):
        return x * self.__gap_x + self.__PLOT_WIDTH / 2

    def __transform_x_inverse(self, x):
        return (x - self.__PLOT_WIDTH / 2) / self.__gap_x

    def __transform_y(self, y):
        return -y * self.__gap_y + self.__PLOT_HEIGHT / 2

    def __transform_y_inverse(self, y):
        return -(y - self.__PLOT_HEIGHT / 2) / self.__gap_y
