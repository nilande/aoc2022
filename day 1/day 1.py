#
# Process input
#
with open('day 1/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
elves = content.split('\n\n')

mostCalories = 0
for elf in elves:
    foods = elf.splitlines()
    calories = sum(int(food) for food in foods)
    if calories > mostCalories: mostCalories = calories

print("Puzzle 1 solution is:", mostCalories)

#
# Puzzle 2
#
elfCalories = list()
for elf in elves:
    foods = elf.splitlines()
    elfCalories.append(sum(int(food) for food in foods))

elfCalories.sort(reverse=True)
topThree = sum(elfCalories[:3])
print("Puzzle 2 solution is:", topThree)