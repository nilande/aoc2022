import re, functools, time

#
# Classes
#
class Blueprint:
    def __init__(self, id: str, blueprint_text: str) -> None:
        self.id = int(id)
        self.recipes = []
        recipes = re.findall(r'Each (.+?) robot costs (.+?)\.', blueprint_text)
        self.max_robots = (0, 0, 0, 0)
        for output_text, inputs_text in recipes:
            match output_text:
                case 'ore': output = (1, 0, 0, 0)
                case 'clay': output = (0, 1, 0, 0)
                case 'obsidian': output = (0, 0, 1, 0)
                case 'geode': output = (0, 0, 0, 1)
            input = [0, 0, 0, 0]
            for quantity, ingredient in map(lambda x: x.split(), inputs_text.split(' and ')):
                match ingredient:
                    case 'ore': input[0] = -int(quantity)
                    case 'clay': input[1] = -int(quantity)
                    case 'obsidian': input[2] = -int(quantity)
                    case 'geode': input[3] = -int(quantity)
            self.max_robots = tuple(max(a, -b) for a, b in zip(self.max_robots, input))
            self.recipes.append((tuple(input), output))

    @functools.cache
    def get_max_geodes(self, inventory: tuple, robots: tuple, time_remaining: int) -> int:
        """Order of each tuple: (ore, clay, obsidian, geode) - regardless of if it is inventory or robots"""
        # If time is up, return captured materials
        if time_remaining == 0:
            # print(f'Ran out of time with inventory {inventory} and robots {robots}')
            return inventory

        # Check what robots can be built with the materials or robots available
        valid_recipes = []
        for recipe in self.recipes:
            recipe_input, recipe_output = recipe
            if any(r*time_remaining+i>=mr*time_remaining for mr, r, ro, i in zip(self.max_robots[:3], robots[:3], recipe_output[:3], inventory[:3]) if ro == 1): continue
            if all(a + b >= 0 for a, b in zip(inventory, recipe_input)):
                valid_recipes.append((recipe_input, recipe_output, 1))
            elif all((r != 0) >= (i != 0) for r, i in zip(robots, recipe_input)):
                mfg_time = max(-((a+b)//c) for a, b, c in zip(inventory, recipe_input, robots) if c>0) + 1
                if mfg_time <= time_remaining: valid_recipes.append((recipe_input, recipe_output, mfg_time))
        if len(valid_recipes) == 0: valid_recipes.append(((0, 0, 0, 0), (0, 0, 0, 0), time_remaining))

        # Iterate over the manufacturing cases
        best_geode_outcome = None
        for recipe_input, recipe_output, mfg_time in valid_recipes:
            # Harvest resources and deduct the cost for the chosen robot
            new_inventory = tuple(a+b+mfg_time*c for a, b, c in zip(inventory, recipe_input, robots))

            # Create the new robots (costs already deducted)
            new_robots = tuple(sum(x) for x in zip(robots, recipe_output))

            # Recurse into next minute and save the inventory with the highest geode count
            recipe_outcome = self.get_max_geodes(new_inventory, new_robots, time_remaining-mfg_time)

            if best_geode_outcome is None or best_geode_outcome[3] < recipe_outcome[3]: best_geode_outcome = recipe_outcome

        return best_geode_outcome

#
# Process input
#
with open('day 19/input.txt') as file:
    contents = file.read()

blueprints = list(map(lambda x: Blueprint(x[0], x[1]), re.findall(r'^Blueprint (\d+):(.*)$', contents, re.MULTILINE)))

#
# Puzzle 1
#
acc = 0
for bp in blueprints:
    start_time = time.time()
    _, _, _, bp_geodes = (bp.get_max_geodes((0, 0, 0, 0), (1, 0, 0, 0), 24))
    acc += bp.id * bp_geodes
    print(f'Result from Blueprint {bp.id}: {bp_geodes} geodes (in {time.time()-start_time:.3f} seconds)')

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
acc = 1
for bp in blueprints[:3]:
    start_time = time.time()
    _, _, _, bp_geodes = (bp.get_max_geodes((0, 0, 0, 0), (1, 0, 0, 0), 32))
    acc *= bp_geodes
    print(f'Result from Blueprint {bp.id}: {bp_geodes} geodes (in {time.time()-start_time:.3f} seconds)')

print(f'Puzzle 2 solution is: {acc}')