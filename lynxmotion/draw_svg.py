from lxml import etree
import sys
import drawing

PAPER_SIZE = (0.1, 0.1) #10cm x 10cm
OFFSET = (-0.05, 0.175) #Where to place the SVG origin

def get_paths(svg):
    nsmap = {'svg': 'http://www.w3.org/2000/svg'}
    paths = []
    relative = False
    for attr in svg.xpath("//svg:path/@d", namespaces=nsmap):
        path = []
        for elem in attr.split():
            #m is a relative moveto command
            if elem[0] == "m":
                relative = True
                continue
            #M is an absolute moveto command
            if elem[0] == "M":
                relative = False
                continue
            if elem[0] == "l":
                relative = True
                continue
            #z means to close the loop
            if elem[0] == "z" or elem[0] == "Z":
                path.append(path[0])
                continue
            x,y = elem.split(',')
            x = float(x)
            y = float(y)
            if relative and path:
                x = x + path[-1][0]
                y = y + path[-1][1]
            path.append((float(x), float(y)))
        paths.append(path)
    return paths

def convert_paths(paths):
    xs = []
    ys = []
    for path in paths:
        for x,y in path:
            xs.append(x)
            ys.append(y)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    #XXX: Assumes the paper is square
    ratio = PAPER_SIZE[0] / max(max_x - min_x, max_y - min_y)

    converted_paths = []
    for path in paths:
        converted = []
        for x,y in path:
            #Remove any offset from the origin (clip blank space)
            cx = (x - min_x)
            #Convert to meters
            cx *= ratio
            cx += OFFSET[0]
            
            #Remove any offset from the origin (clip blank space)
            cy = (y - min_y)
            #Convert to meters
            cy *= ratio
            cy += OFFSET[1]
            converted.append((cx,cy))
        converted_paths.append(converted)
    return converted_paths



if __name__ == "__main__":
    svg = etree.XML(open(sys.argv[1]).read())
    inp = raw_input("Place_pen? (y/n)")
    d = drawing.Drawing()
    if inp.startswith("y"):
        d.init()
        inp = raw_input("Press enter when done")
    d.grip_pen()
    paths = get_paths(svg)
    for path in convert_paths(paths):
        d.path(path)

