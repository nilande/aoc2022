FROM_SNAFU = { '=': -2, '-': -1, '0': 0, '1': 1, '2': 2 }
TO_SNAFU = { -2: '=', -1: '-', 0: '0', 1: '1', 2: '2' }

#
# Helper functions
#
def from_snafu(snafu: str) -> int:
    result = 0
    for i, c in enumerate(snafu[::-1]):
        result += 5 ** i * FROM_SNAFU[c]
    return result

def to_snafu(num: int) -> str:
    snafu = ''
    while num != 0:
        dig = num % 5
        if dig > 2: dig -= 5
        snafu += TO_SNAFU[dig]
        num -= dig
        num //= 5
    return snafu[::-1]

#
# Process input
#
with open('day 25/input.txt') as file:
    snafus = file.read().splitlines()

#
# Puzzle
#
acc = 0
for snafu in snafus: acc += from_snafu(snafu)
print(f'Puzzle result is {to_snafu(acc)}')