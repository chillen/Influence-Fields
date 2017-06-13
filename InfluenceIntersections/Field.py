import math
import Tools

class Field():
    def __init__(self, tag, colour, wide, spread, location, interference=[]):
        self.tag = tag
        self.colour = colour
        self.wide = wide
        self.spread = spread
        self.location = location
        self.interference = interference
        self.data = None
    
    # 400 is the current normalize. Shush, this is a quick demo
    def _field_at(self, x, y):
        r = math.hypot(self.location[0] - x, self.location[1] - y)
        r = r/400
        f = self.spread * math.exp(-self.wide * r**2)
        for i in self.interference:
            f -= i[1] * math.exp(-i[0] * r**2)
            
        return f
    
    # Requires optimization
    # Returns a map of values this field generates
    # Takes in max height and max width
    def emit(self, H, W):
        out = [ [ 0 for _ in range(H) ] for _ in range(W) ]
        for x in range(W):
            for y in range(H):
                out[x][y] = min(self._field_at(x, y), Tools.FIELD_MAX)
        self.data = out
        return out