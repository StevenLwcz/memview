NL = "\n"

GREEN = "\x1b[38;5;47m"
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
        if len(arguments) == 0:
            print("memview expression")
            return

        self.win.set_display(arguments)

memViewCmd = MemViewCmd()

class MemViewWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Memory View"
        self.buff = ""

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.write(self.buff, True)

    def set_display(self, args):
        self.tui.title = args

        expr = gdb.parse_and_eval(args)
        if expr.address == None:
            addr = expr
        else:
            addr = expr.address

        n = self.tui.height * 8
        infe = gdb.selected_inferior()
        mv = infe.read_memory(addr, n)

        self.buff = ""
        for i in range(0, n, 8):
            m = mv[i:i + 8]
            text = pattern.sub('.', m.tobytes().decode('latin-1'))
            self.buff+=f"{hex(addr + i)}: {m.hex(' ')} {text}\n"

        self.render()

    def close(self):
        pass

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        print(x, y, button)
        pass
 
# Factory Method
def MemViewFactory(tui):
    win = MemViewWindow(tui)
    memViewCmd.set_win(win)
    return win

gdb.register_window_type("memview", MemViewFactory)
