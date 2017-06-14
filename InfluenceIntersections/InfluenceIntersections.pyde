from Field import Field
from Location import Location 
import math
import copy
import Tools

# The max radius of a field is a power series about the stddev
# Given the stddev, b, the max radius (where the field is >= 1) 
# is equal to f(4.761 * sqrt(b))

map_data = []
map_points = []
click_points = []

W = 600
H = 500
VIEW = ceil(math.sqrt((W**2 + H**2)))

canvas = createImage(W,H,RGB)

COL_BG = (20,20,20)
SIZE_POINT = 10

def setup():
    size(10,10)
    this.surface.setSize(W+VIEW,H)
    setup_canvas()
    setup_data()
    update_fields()
    draw_data()
    cursor(CROSS)

def draw():
    background(0)
    image(canvas, 0, 0)
    draw_points()
    draw_clicks()
    draw_line()
    draw_waves()
    
def setup_canvas():
    canvas.loadPixels()
    canvas.pixels = [color(*COL_BG) for p in canvas.pixels]
    canvas.updatePixels()

def draw_data():
    for loc in map_points:
        for field in loc.fields:
            for i, c in enumerate(canvas.pixels):
                x = int(i % W)
                y = int(math.floor(float(i) / W))
                if field.location[0] - field.radius < x < field.location[0] + field.radius:
                    if field.location[1] - field.radius < y < field.location[1] + field.radius:
                        _r = red(c)
                        _g = green(c)
                        _b = blue(c)
                        _r += (float(field.colour[0]) / 256) * field.data[x][y]
                        _g += (float(field.colour[1]) / 256) * field.data[x][y]
                        _b += (float(field.colour[2]) / 256) * field.data[x][y]
                        canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()
    
def draw_grid(inc=10):
    stroke(40)
    strokeWeight(1)
    for i in range(W, W+VIEW, inc):
        line(i, 0, i, H)
    for i in range(0, H, inc):
        line(W, i, W+VIEW, i)
    
# Based on RedBlob linear interpolation
def pixels_between(points):
    def round_point(p):
        return (int(round(p[0])), int(round(p[1])))
    def diag_dist(points):
        dx = points[0][0] - points[1][0]
        dy = points[1][0] - points[0][1]
        return max(abs(dx), abs(dy))
    def lerp(s, e, t):
        return s + t * (e-s)
    def lerp_points(points, t):
        return ( lerp(points[0][0], points[1][0], t), lerp(points[0][1], points[1][1], t) )
    on_line = []
    N = diag_dist(points)
    if N == 0:
        return
    for i in range(N):
        t = float(i)/N
        on_line.append(round_point(lerp_points(points, t)))
    return on_line

def draw_waves():
    # Grid lines
    draw_grid()
    if len(click_points) != 2:
        return
    sorted_clicks = copy.copy(click_points)
    sorted_clicks.sort(key=lambda p: p[0])
    points = pixels_between(sorted_clicks)
    strokeWeight(2)
    stroke(255)
    if len(points) < 2:
        return
    
    for loc in map_points:
        for field in loc.fields:
            draw_field_wave(field, points)

def draw_field_wave(field, points):
    points = [(i, field.data[p[0]][p[1]]) for i,p in enumerate(points)]
    points = [(p[0] + W, H - (H*p[1]/(Tools.FIELD_MAX+13))) for p in points]
    stroke(*field.colour)
    strokeWeight(2)
    noFill()
    beginShape()
    curveVertex(*points[0])
    for p in points:
        curveVertex(*p)
    curveVertex(*points[-1])
    endShape();

def draw_points():
    ellipseMode(CENTER)
    noStroke()
    for p in map_points:
        fill(*p.colour)
        ellipse(p.x, p.y, SIZE_POINT, SIZE_POINT)
        
def draw_clicks():
    cross_length = 5
    for p in click_points:
        strokeWeight(1)
        stroke(0)
        line(p[0]-cross_length, p[1], p[0]+cross_length, p[1])
        line(p[0], p[1]-cross_length, p[0], p[1]+cross_length)

def draw_line():
    if len(click_points) == 2:
        strokeWeight(1)
        stroke(220,200,50)
        line(click_points[0][0], click_points[0][1], click_points[1][0], click_points[1][1])
        
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
    i = []
    map_points.append(Location((W/2, H/2), (20,100,40)))
    map_points[-1].add_field('green', (20,100,40), 100, Tools.FIELD_MAX, i)
    
def mouseDragged():
    global click_points
    if mouseX > W:
        return
    click_points[1] = (mouseX, mouseY)
    
def mousePressed():
    if mouseX > W:
        return
    if mouseButton == LEFT:
        global click_points
        click_points = [ (mouseX, mouseY), (mouseX, mouseY) ]
    else:
        x = int(round(mouseX))
        y = int(round(mouseY))
        for loc in map_points:
            for field in loc.fields:
                print("{:}: {:.2f}".format(field.tag, field.data[x][y]))
    