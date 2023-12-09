#
# Process input
#
with open('day 10/input.txt', 'r') as file:
    lines = list(map(lambda x: x.split(), file.read().splitlines()))

#
# Puzzle 1
#
tests = [i for i in range(20, 221, 40)]
cycle = 0
register = 1
acc = 0

for line in lines:
    if len(tests) == 0: break
    match line[0]:
        case 'addx':
            cycle += 2
            if cycle >= tests[0]:
                acc += tests[0] * register
                tests = tests[1:]
            register += int(line[1])
        case 'noop':
            cycle += 1

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
def get_pixel(cycle, register):
    if abs(register - cycle) < 2: return 'o'
    else: return ' '

cycle = 0
register = 1
pixels = ''
for line in lines:
    pixels += get_pixel((cycle%40), register)
    match line[0]:
        case 'addx':
            cycle += 2
            pixels += get_pixel((cycle-1) % 40, register)
            register += int(line[1])
        case 'noop':
            cycle += 1

print(f'Puzzle 2 solution is:')
print(pixels[0:40])
print(pixels[40:80])
print(pixels[80:120])
print(pixels[120:160])
print(pixels[160:200])
print(pixels[200:240])
