import re, math, functools

#
# Process input
#
with open('day 11/input.txt', 'r') as file:
    content = file.read()

worry_levels = list(map(lambda x: list(map(int, x.split(', '))), re.findall(r'Starting items: (.*)', content, re.MULTILINE)))
operations = list(map(lambda x: x.split(), re.findall(r'Operation: new = (.*)', content, re.MULTILINE)))
divisors = list(map(int, re.findall(r'Test: divisible by (\d*)', content, re.MULTILINE)))
true_destinations = list(map(int, re.findall(r'If true: throw to monkey (\d+)', content, re.MULTILINE)))
false_destinations = list(map(int, re.findall(r'If false: throw to monkey (\d+)', content, re.MULTILINE)))

def calculate_new_worry_level(worry_level, operation):
    operation = [str(worry_level) if item == 'old' else item for item in operation]
    match operation[1]:
        case '+': return int(operation[0]) + int(operation[2])
        case '*': return int(operation[0]) * int(operation[2])

#
# Puzzle 1
#
inspection_counts = [0] * len(worry_levels)
for round_no in range(20):
    for monkey_no in range(len(worry_levels)):
        for item_no in range(len(worry_levels[monkey_no])):
            inspection_counts[monkey_no] += 1
            new_worry_level = calculate_new_worry_level(worry_levels[monkey_no][0], operations[monkey_no]) // 3
            worry_levels[monkey_no] = worry_levels[monkey_no][1:]
            match new_worry_level % divisors[monkey_no] == 0:
                case True: worry_levels[true_destinations[monkey_no]].append(new_worry_level)
                case False: worry_levels[false_destinations[monkey_no]].append(new_worry_level)

inspection_counts.sort(reverse=True)

print(f'Puzzle 1 solution is: {inspection_counts[0] * inspection_counts[1]}')

#
# Puzzle 2
#
big_divisor = functools.reduce(math.lcm, divisors)
worry_levels = list(map(lambda x: list(map(int, x.split(', '))), re.findall(r'Starting items: (.*)', content, re.MULTILINE)))
inspection_counts = [0] * len(worry_levels)
for round_no in range(10000):
    for monkey_no in range(len(worry_levels)):
        for item_no in range(len(worry_levels[monkey_no])):
            inspection_counts[monkey_no] += 1
            new_worry_level = calculate_new_worry_level(worry_levels[monkey_no][0], operations[monkey_no]) % big_divisor
            worry_levels[monkey_no] = worry_levels[monkey_no][1:]
            match new_worry_level % divisors[monkey_no] == 0:
                case True: worry_levels[true_destinations[monkey_no]].append(new_worry_level)
                case False: worry_levels[false_destinations[monkey_no]].append(new_worry_level)

inspection_counts.sort(reverse=True)

print(f'Puzzle 2 solution is: {inspection_counts[0] * inspection_counts[1]}')