with open("a.txt", 'r') as fpff:
    a = fpff.read()

with open("b.txt", 'r') as fpff:
    b = fpff.read()

out = ""
actr = 0
bctr = 0
while True:
    ach = a[actr]
    bch = b[bctr]

    if ach == bch:
        actr += 1
        bctr += 1
    elif ach != bch:
        out = out + ach

        if actr + 1 == len(a) or bctr + 1 == len(b):
            break

        if a[actr + 1] == b[bctr + 1]:
            actr += 1
            bctr += 1
        else:
            actr += 1

print(out)