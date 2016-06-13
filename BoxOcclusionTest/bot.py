import sys


def fill(x, y, width, height):
    print('(%s,%s) => (%s,%s)' % (x, y, x + width, y + height))


def main(argv):
    print('Box Occlusion Test')

    width = 200
    height = 300

    curx = 500
    cury = 500

    print('Box right 10px')
    newx = curx + 10
    newy = cury
    blank(curx, cury, newx, newy, width, height)

    print('Box left 10px')
    newx = curx - 10
    newy = cury
    blank(curx, cury, newx, newy, width, height)

    print('Box up 10px')
    newx = curx
    newy = cury - 10
    blank(curx, cury, newx, newy, width, height)

    print('Box down 10px')
    newx = curx
    newy = cury + 10
    blank(curx, cury, newx, newy, width, height)

    print('Box down right 10px')
    newx = curx + 10
    newy = cury + 10
    blank(curx, cury, newx, newy, width, height)

    print('Box down left 10px')
    newx = curx - 10
    newy = cury + 10
    blank(curx, cury, newx, newy, width, height)

    print('Box up right 10px')
    newx = curx + 10
    newy = cury - 10
    blank(curx, cury, newx, newy, width, height)

    print('Box up left 10px')
    newx = curx - 10
    newy = cury - 10
    blank(curx, cury, newx, newy, width, height)


def blank(x, y, newx, newy, width, height):
    blankcol(x, y, newx, newy, width, height)
    blankrow(x, y, newx, newy, width, height)

def blankcol(x, y, newx, newy, width, height):
    blankx = x
    blanky = y
    blankheight = height

    if newx > x:
        blankwidth = newx - x
        fill(blankx, blanky, blankwidth, blankheight)
    elif newx < x:
        blankwidth = x - newx
        blankx = newx + width
        fill(blankx, blanky, blankwidth, blankheight)


def blankrow(x, y, newx, newy, width, height):
    blankx = x
    blanky = y
    blankwidth = width

    if newy > y:
        blankheight = newy - y
        fill(blankx, blanky, blankwidth, blankheight)
    elif newy < y:
        blankheight = y - newy
        blanky = newy + height
        fill(blankx, blanky, blankwidth, blankheight)


if __name__ == '__main__':
    main(sys.argv[1:])
