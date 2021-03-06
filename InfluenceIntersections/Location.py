# Locations contain multiple field generators
# They contain a colour to differentiate themselves 
# They contain an x,y to pass along to the field generators

from Field import Field

class Location():
    def __init__(self, loc, colour):
        self.location = loc
        self.x = loc[0]
        self.y = loc[1]
        self.fields = []
        self.colour = colour
        
    def add_field(self, name, colour, radius, peak, interference=[]):
        self.fields.append(Field(name, colour, radius, peak, self.location, interference))
        
    def num_fields(self):
        return len(self.fields)