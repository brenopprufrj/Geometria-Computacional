import math
import random

EPSILON = 1e-9
ROT_ANGLE = 1e-4
PERTURB = 1e-7
HAS_ROTATED = 0

def orient(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Point(self.x * cos_a - self.y * sin_a,
                     self.x * sin_a + self.y * cos_a)

    def perturbed(self):
        return Point(self.x + random.uniform(-PERTURB, PERTURB),
                     self.y + random.uniform(-PERTURB, PERTURB))

    def __repr__(self):
        return f"({self.x:.6f},{self.y:.6f})"

class IncrementalConvexHull:
    def __init__(self, points):
        self.points = [Point(*pt) if not isinstance(pt, Point) else pt for pt in points]
        self.hull = []

    def preprocess(self):
        xs = [p.x for p in self.points]
        if len(xs) != len(set(xs)):
            self.points = [p.rotate(ROT_ANGLE) for p in self.points]
            HAS_ROTATED == 1
        self.points.sort(key=lambda p: (p.x, p.y))
        if HAS_ROTATED == 1:
            self.points = [p.rotate(-ROT_ANGLE) for p in self.points]

    def init_hull(self):
        p0, p1, p2 = self.points[0], self.points[1], self.points[2]
        if abs(orient(p0, p1, p2)) < EPSILON:
            p2 = p2.perturbed()
        if orient(p0, p1, p2) > 0:
            p1, p2 = p2, p1
        self.hull = [p0, p1, p2]

    def is_inside(self, p):
        n = len(self.hull)
        for i in range(n):
            a = self.hull[i]
            b = self.hull[(i + 1) % n]
            if orient(a, b, p) < -EPSILON:
                return False
        return True

    def add_point(self, p):
        if self.is_inside(p):
            return

        n = len(self.hull)
        visible = [i for i in range(n) if orient(self.hull[i], self.hull[(i + 1) % n], p) >= -EPSILON]
        
        if len(visible) > 1:
            for idx in visible[::-1][:-1]:
                del self.hull[idx]

        self.hull.insert(visible[0] + 1, p)

    def compute(self):
        self.preprocess()
        self.init_hull()
        for p in self.points[3:]:
            self.add_point(p)
        return self.hull

if __name__ == "__main__":
    pts = input("Insira seus pontos no formato [(a,b), (c,d), (e,f)...]\n")
    pts = eval(pts)
    print(f"Gerando hull para {len(pts)} pontos...")
    hull_solver = IncrementalConvexHull(pts)
    hull = hull_solver.compute()
    print("Convex Hull encontrado:")
    print(hull)
