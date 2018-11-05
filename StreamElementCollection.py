from FreeStream import FreeStream
from Source import Source
from ElementTypes import ElementTypes


class StreamElementCollection:
    def __init__(self, canvas, watcher):
        self.plot = canvas
        self.__sources = {}
        self.free_stream = FreeStream(self.plot, 0, 0)
        self.watcher = watcher

    def get_source(self, tag):
        return self.__sources[tag]

    def get_all_sources(self):
        return self.__sources.values()

    def get_free_stream(self):
        return self.free_stream

    def add_source(self, tag, m, x, y):
        s = Source(self.plot, tag, m, x, y, ElementTypes["source"], self.watcher)
        self.__sources[tag] = s
        s.draw()

        return s

    def add_free_stream(self, u_inf, alpha):
        self.free_stream = FreeStream(self.plot, u_inf, alpha)

    def delete_source(self, tag):
        self.__sources[tag].erase()
        del self.__sources[tag]
