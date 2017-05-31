from Field import Field
from Location import Location 
import math

map_data = []
map_points = []

W = 400
H = 400

canvas = createImage(W,H,RGB)

COL_BG = (50,200,100)
SIZE_POINT = 10

def setup():
    size(10,10)
    this.surface.setSize(W,H)
    setup_canvas()
    setup_data()
    update_fields()
    draw_data()

def draw():
    image(canvas, 0, 0)
    draw_points()
    
def setup_canvas():
    canvas.loadPixels()
    canvas.pixels = [color(*COL_BG) for p in canvas.pixels]
    canvas.updatePixels()

# Not accurately drawing
# TODO: colourize correctly, draw each field properly
def draw_data():
    for i, c in enumerate(canvas.pixels):
        count = 0.0
        x = i % W
        y = math.floor(float(i) / W)
        count += map_data[int(x)][int(y)][0]
        _r = red(c)
        _g = green(c)
        _b = blue(c)
        _r += count
        _g -= count
        canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()
    
def draw_points():
    ellipseMode(CENTER)
    noStroke()
    for p in map_points:
        fill(*p.colour)
        ellipse(p.x, p.y, SIZE_POINT, SIZE_POINT)
        
# Uses this awesome flatten comprehension: https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(to_flatten):
    return [item for sublist in to_flatten for item in sublist]

def update_fields():
    global map_data
    all_fields = flatten([p.fields for p in map_points])
    for i,f in enumerate(all_fields):
        out = f.emit(H,W)
        for x in range(len(out)):
            for y in range(len(out[x])):
               map_data[x][y][i] = out[x][y]
    
def setup_data():
    global map_data
    setup_points()
    num_fields = 0
    for p in map_points:
        num_fields += p.num_fields()
    map_data = [ [ [0 for _ in range(num_fields)] for _ in range(H)] for _ in range(W) ]
    
def setup_points():
    global map_points
    map_points = []
    map_points.append(Location((50,50), (20,100,40)))
    map_points[-1].add_field('war', (20,100,40), 300, 500)
    map_points.append(Location((150,150), (200,200,140)))
    map_points[-1].add_field('water', (20,50,200), 300, 500)
    map_points.append(Location((200,300), (0,200,200)))