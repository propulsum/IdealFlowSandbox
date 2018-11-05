import math


class IdealFlowCalculator:
    def __init__(self, scale, stream_elements):
        self.scale = scale
        self.StreamElements = stream_elements

    def u(self, x, y):
        u_inf = 0
        u = u_inf
        for source in self.StreamElements.get_all_sources():
            u += source.u(x, y)

        return u

    def v(self, x, y):
        u_inf = 0
        v = u_inf
        for source in self.StreamElements.get_all_sources():
            v += source.v(x, y)

        return v

    def normalize(self, v):
        mag = self.magnitude(v)

        v[0] = v[0] / mag / (self.scale / 5)
        v[1] = v[1] / mag / (self.scale / 5)

        return v, mag

    def magnitude(self, v):
        return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

    def get_streamline(self, r):
        points = []
        u = [0, 0]
        need_to_break = False
        for i in range(1000):
            u[0] = self.u(r[0], r[1])
            u[1] = self.v(r[0], r[1])

            u, mag = self.normalize(u)

            p = [r[0], r[1], mag]

            points.append(p)

            if need_to_break:
                break

            r[0] = r[0] + u[0]
            r[1] = r[1] + u[1]

            if self.is_near_sink(r):
                need_to_break = True

        return points

    def is_near_sink(self, p):
        e = .1
        for s in self.StreamElements.get_all_sources():
            if s.m < 0:
                rx = abs(s.x - p[0])
                ry = abs(s.y - p[1])

                if self.magnitude([rx, ry]) < e:
                    return True
        return False
