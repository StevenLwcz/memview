NL = "\n"

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
RESET = "\x1b[0m"


import re
pattern = re.compile(r'[\x00-\x1f\x7f-\x9f]')

class MemViewCmd(gdb.Command):
    """memview expression
Memory view at the address of the expression"""

    def __init__(self):
        super(MemViewCmd, self).__init__("memview", gdb.COMMAND_USER)
        self.win = None

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        if self.win == None: 
            print("memview: run 'layout memview' to set up Tui mode")
            return

        if len(arguments) == 0:
            print("memview: expression")
            return

        try:
            expr = gdb.parse_and_eval(arguments)
        except gdb.Error:
            print("memview: can't evaluate {arguments}")
            return

        if expr.address == None:
            addr = expr
        else:
            addr = expr.address

        self.win.set_title(arguments)
        self.win.set_display(addr)

memViewCmd = MemViewCmd()

class MemViewWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Memory View"
        self.buff = "Nothing to display"
        self.addr = 0

    def set_title(self, args):
        self.tui.title = args

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.write(self.buff, True)

    def set_display(self, addr):
        self.addr = addr
        infe = gdb.selected_inferior()
        n = self.tui.height * 8
        mv = infe.read_memory(addr, n)

        self.buff = ""
        for i in range(0, n, 8):
            m = mv[i:i + 8]
            text = pattern.sub('.', m.tobytes().decode('latin-1'))
            self.buff+=f"{GREEN}{hex(addr + i)}: {BLUE}{m.hex(' ')}{RESET} {text}\n"

        self.render()

    def close(self):
        pass

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        addr = self.addr + num * 8
        self.set_display(addr)
        pass

    def click(self, x, y, button):
        pass
 
# Factory Method
def MemViewFactory(tui):
    win = MemViewWindow(tui)
    memViewCmd.set_win(win)
    return win

gdb.register_window_type("memview", MemViewFactory)
