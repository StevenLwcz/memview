# Blog Part 1

NL = "\n"

GREEN = "\x1b[38;5;47m"
RESET = "\x1b[0m"

import re
pattern = re.compile(r'[\x00-\x1f\x7f-\x9f]')

# Factory Method
def MemViewFactory(tui):
    return MemViewWindow(tui)

class MemViewWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Hello Window"
        self.buff = ""

    def render(self):
        if not self.tui.is_valid():
            return

        self.set_display()
        self.tui.write(self.buff, True)

    def set_display(self):

        expr = gdb.parse_and_eval("a")
        if expr.address == None:
            addr = expr
        else:
            addr = expr.address

        infe = gdb.selected_inferior()
        mv = infe.read_memory(addr, 32)

        self.buff = ""
        for i in range(0, 32, 8):
            m = mv[i:i + 8]
            text = pattern.sub('.', m.tobytes().decode('latin-1'))
            self.buff+=f"{hex(addr + i)}: {m.hex(' ')} {text}\n"

        # render()

    def close(self):
        pass

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        print(x, y, button)
        pass
 
gdb.register_window_type("memview", MemViewFactory)
