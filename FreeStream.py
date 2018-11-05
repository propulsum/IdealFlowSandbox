import math


class FreeStream:
    def __init__(self, master, u_inf, alpha):
        self.master = master

        self.u_inf = u_inf
        self.alpha = alpha

    def u(self):
        return self.u_inf * math.cos(self.alpha)

    def v(self):
        return self.u_inf * math.sin(self.alpha)


