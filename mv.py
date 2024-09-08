expr = gdb.parse_and_eval("a")
if expr.address == None:
    addr = expr
else:
    addr = expr.address

print(hex(int(addr)))

infe = gdb.selected_inferior()
mv = infe.read_memory(addr, 32)
print(mv.hex(' '))

import re
pattern = re.compile(r'[\x00-\x1f\x7f-\x9f]')

text = mv.tobytes().decode('latin-1')
text =  pattern.sub('.', text)

print(text)

for i in range(0, 32, 8):
    m = mv[i:i + 8]
    text = pattern.sub('.', m.tobytes().decode('latin-1'))
    print(f"{hex(addr + i)}: {m.hex(' ')} {text}")
