import math
import Tools

class Field():
    def __init__(self, tag, colour, radius, peak, location, interference=[]):
        self.tag = tag
        self.colour = colour
        self.radius = radius
        self.peak = peak
        self.location = location
        self.interference = interference
        self.data = None
    
    def _field_at(self, x, y):
        r = (self.location[0] - x)**2 + (self.location[1] - y)**2
        stdev = (self.radius / 4.761)**2
        f = self.peak * math.exp(-stdev**(-1) * r)
        for i in self.interference:
            stdev = (i[0]/4.761)**2
            f -= i[1] * math.exp(-stdev * r)
            
        return f
    
    # Requires optimization
    # Returns a map of values this field generates
    # Takes in max height and max width
    def emit(self, H, W):
        out = [ [ 0 for _ in range(H) ] for _ in range(W) ]
        for x in range(self.x-self.radius, self.x+self.radius):
            for y in range(self.y-self.radius, self.y+self.radius):
                out[x][y] = min(self._field_at(x, y), Tools.FIELD_MAX)
        self.data = out
        return out