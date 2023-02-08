
import curses

for x in dir(curses):
    if x.startswith('KEY_'):
        exec(f'{x} = curses.{x}')
MOUSE = curses.KEY_MOUSE

def start():
    '''start the window'''
    global s
    s = curses.initscr()
    curses.noecho()
    curses.cbreak()
    s.keypad(True)
    global BLACK, WHITE, RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA, COLORS
    curses.use_default_colors()
    BLACK = curses.COLOR_BLACK
    WHITE = curses.COLOR_WHITE
    RED = curses.COLOR_RED
    YELLOW = curses.COLOR_YELLOW
    GREEN = curses.COLOR_GREEN
    CYAN = curses.COLOR_CYAN
    BLUE = curses.COLOR_BLUE
    MAGENTA = curses.COLOR_MAGENTA
    COLORS = (BLACK, WHITE, RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA)
    for bg in COLORS:
        for fg in COLORS:
            curses.init_pair(bg + (8 * fg), bg, fg)

def stop():
    '''stop the window'''
    curses.nocbreak()
    global s
    s.keypad(False)
    curses.echo()

def handle(func):
    '''internal function'''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except curses.error as e:
            stop()
            raise e

@handle
def clear():
    '''clear window'''
    global s
    s.clear()

@handle
def update():
    '''update window'''
    global s
    s.update()

@handle
def getf(bg=None, fg=None, blink=False, bold=False, dim=False, \
        reverse=False, highlight=False, ul=False):
    '''get formatting'''
    global BLACK, WHITE
    if bg == None: bg = BLACK
    if fg == None: fg = WHITE
    a = curses.A_BLINK if blink else 0
    b = curses.A_BOLD if bold else 0
    c = curses.A_DIM if dim else 0
    d = curses.A_REVERSE if reverse else 0
    e = curses.A_STANDOUT if highlight else 0
    f = curses.A_UNDERLINE if ul else 0
    return curses.get_color(bg + (fg * 8) ^ a ^ b ^ c ^ d ^ e ^ f)    

@handle
def draw(t, x=None, y=None, f=None):
    '''draw t at x and y with formatting f'''
    global s
    if x == None or y == None:
        if f == None:
            s.addstr(t)
        else:
            s.addstr(t, f)
    elif x == None or y == None:
        raise ValueError('Cannot have just 1 coordinate defined')
    else:
        if f == None:
            s.addstr(y, x, t)
        else:
            s.addstr(y, x, t, f)

@handle
def inp():
    '''outputs either character or integer from keyboard input, use constants to detect'''
    global s
    if x < 255:
        return chr(x)
    else:
        return x

@handle
def inp_block(flag):
    curses.nodelay(flag)
    
def mouse():
    x = curses.getmouse()
    return (x[1], x[2])


















