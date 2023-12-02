#
# Process input
#
with open('day 2/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
points = {
    'A X': 4, # Rock vs. rock(1) = draw(3)
    'A Y': 8, # Rock vs. paper(2) = win(6)
    'A Z': 3, # Rock vs. scissors(3) = loss(0)
    'B X': 1, # Paper vs. rock(1) = loss(0)
    'B Y': 5, # Paper vs. paper(2) = draw(3)
    'B Z': 9, # Paper vs. scissors(3) = win(6)
    'C X': 7, # Scissors vs. rock(1) = win(6)
    'C Y': 2, # Scissors vs. paper(2) = loss(0)
    'C Z': 6 # Scissors vs. scissors(3) = draw(3)
}

acc = 0
for round in content.splitlines():
    acc += points[round]

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
points = {
    'A X': 3, # Rock vs. scissors(3) = loss(0)
    'A Y': 4, # Rock vs. rock(1) = draw(3)
    'A Z': 8, # Rock vs. paper(2) = win(6)
    'B X': 1, # Paper vs. rock(1) = loss(0)
    'B Y': 5, # Paper vs. paper(2) = draw(3)
    'B Z': 9, # Paper vs. scissors(3) = win(6)
    'C X': 2, # Scissors vs. paper(2) = loss(0)
    'C Y': 6, # Scissors vs. scissors(3) = draw(3)
    'C Z': 7 # Scissors vs. rock(1) = win(6)
}

acc = 0
for round in content.splitlines():
    acc += points[round]

print("Puzzle 2 solution is:", acc)
