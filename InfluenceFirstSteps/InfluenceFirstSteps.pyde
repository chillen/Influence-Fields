import math
import time
from random import shuffle

# Std dev changes the width
# Splat based on std dev
# Broadcast from center
# Add ability to draw cross section; draw a line, see what the graph looks like across that line
# Emphasize fixed structures (cathedral, bridge)
# Sum the minimum (integrate) to show how much integration is between
# Go from field to toy example of what would the name be
# Turn off influence
# Distance transform as interference point for rivers, mountains
# Start with a breakdown of how things are named and use that to look at comparable fields

point_size = 10
W = 400
H = 400
a = 300.0
b = 1.011
_norm = W
points = [(W/2-50, H/2), (W/2+20,H/2), (W/3-50, H/2+H/4)]

canvas = createImage(W,H,RGB)

def setup():
    size(10,10)
    this.surface.setSize(W,H)
    load_config()
    setup_canvas()

def draw():
    image(canvas, 0,0)
    draw_points()
    
def setup_canvas():
    canvas.loadPixels()
    canvas.pixels = [color(50,200,100) for p in canvas.pixels]
    canvas.updatePixels()
    image(canvas, 0,0)
    
def update_field_random():
    for _ in range(2):
        for i, c in enumerate(canvas.pixels):
            shuffle(points)
            for p in points:
                x = i % W
                y = math.floor(float(i) / W)
                func = field_func(p, (x,y), a, b)
                _r = red(c)
                _g = green(c)
                _b = blue(c)
                _r += func
                _g -= func
                canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()
    
def update_field_iterative():
    for p in points: 
        for i, c in enumerate(canvas.pixels):
            x = i % W
            y = math.floor(float(i) / W)
            func = field_func(p, (x,y), a, b)
            _r = red(c)
            _g = green(c)
            _b = blue(c)
            _r += func
            _g -= func
            canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()

def update_field():
    for i, c in enumerate(canvas.pixels):
        count = 0.0
        x = i % W
        y = math.floor(float(i) / W)
        for p in points:
            count += field_func(p, (x,y), a, b)
        _r = red(c)
        _g = green(c)
        _b = blue(c)
        _r += count
        _g -= count
        canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()

def update_field_noise():
    for i, c in enumerate(canvas.pixels):
        count = 0.0
        x = i % W
        y = math.floor(float(i) / W)
        count += noise(x,y)*200
        _r = red(c)
        _g = green(c)
        _b = blue(c)
        _r += count
        _g -= count
        canvas.pixels[i] = color(_r,_g,_b)
    canvas.updatePixels()

def draw_points():
    ellipseMode(CENTER)
    fill(255)
    noStroke()
    for p in points:
        ellipse(p[0], p[1], point_size, point_size)            

def dispatch(num):
    setup_canvas()
    load_config()
    funcs = {'1':update_field,'2':update_field_iterative,'3':update_field_random,'4':update_field_noise}
    if num not in funcs:
        print "Error: Update function " + num + " not found."
        return
    print "Dispatching function " + num
    print "Running..."
    start = time.time()
    funcs[num]()
    end = time.time()
    print("Function complete. Elapsed time: " + (str(end-start)))

def field_func(key_point, curr_point, a, b):
    r = math.hypot(key_point[0] - curr_point[0], key_point[1] - curr_point[1])
    r = r/_NORM
    return a * math.exp(-b * r**2)



def keyPressed():
    if key == BACKSPACE:
        setup_canvas()
    else:
        print "Pressed: " + key
        dispatch(key)