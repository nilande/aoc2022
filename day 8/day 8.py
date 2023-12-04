#
# Process input
#
with open('day 8/input.txt', 'r') as file:
    content = file.read().splitlines()

height = len(content)
width = len(content[0])

#
# Puzzle 1
#

# Set of visible from left
left = set()
for i in range(height):
    row = content[i]
    limit = -1
    for j in range(width):
        col = int(row[j])
        if col > limit:
            limit = col
            left.add((i, j))

# Set of visible from right
right = set()
for i in range(height):
    row = content[i]
    limit = -1
    for j in range(width-1, -1, -1):
        col = int(row[j])
        if col > limit:
            limit = col
            right.add((i, j))

# Set of visible from top
top = set()
for j in range(width):
    limit = -1
    for i in range(height):
        col = int(content[i][j])
        if col > limit:
            limit = col
            top.add((i, j))

# Set of visible from bottom
bottom = set()
for j in range(width):
    limit = -1
    for i in range(height-1, -1, -1):
        col = int(content[i][j])
        if col > limit:
            limit = col
            bottom.add((i, j))

visible = left | right | top | bottom

print("Puzzle 1 solution is:", len(visible))

#
# Puzzle 2
#
def scenicScore(i, j):
    h = int(content[i][j])
    # Up
    acc = 0
    for y in range(i-1, -1, -1):
        acc +=1
        if int(content[y][j]) >= h:
            break
    score = acc

    # Down
    acc = 0
    for y in range(i+1, height):
        acc +=1
        if int(content[y][j]) >= h:
            break
    score *= acc

    # Left
    acc = 0
    for x in range(j-1, -1, -1):
        acc +=1
        if int(content[i][x]) >= h:
            break
    score *= acc

    # Right
    acc = 0
    for x in range(j+1, width):
        acc +=1
        if int(content[i][x]) >= h:
            break
    score *= acc

    return score

maxScore = 0
for i in range(1, height-1):
    for j in range(1, width-1):
        score = scenicScore(i, j)
        if maxScore < score: maxScore = score

print("Puzzle 2 solution is:", maxScore)