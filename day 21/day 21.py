#
# Classes
#
class Monkey:
    def __init__(self, init_string: str) -> None:
        self.name, self.equation = init_string.split(': ')

    def __repr__(self) -> str:
        return f'{self.name}*'

    def connect(self, others: dict) -> None:
        self.others = others

    def evaluate(self) -> int:
        match self.equation.split():
            case [a, '+', b]:
                return self.others[a].evaluate() + self.others[b].evaluate()
            case [a, '-', b]:
                return self.others[a].evaluate() - self.others[b].evaluate()
            case [a, '*', b]:
                return self.others[a].evaluate() * self.others[b].evaluate()
            case [a, '/', b]:
                return self.others[a].evaluate() // self.others[b].evaluate()
            case [n]:
                return int(n)
            
    def can_evaluate(self) -> bool:
        """Determine which branches of this binary tree that can be evaluated"""
        if self.name == "humn": return False
        match self.equation.split():
            case [a, _, b]:
                self.can_a = self.others[a].can_evaluate()
                self.can_b = self.others[b].can_evaluate()
                return self.can_a and self.can_b
            case [n]: return True

    def force_evaluate(self) -> int:
        """Force evaluation of this binary tree. Assumes this node has '=' operation"""
        a, _, b = self.equation.split()
        if self.can_a:
            a_val = self.others[a].evaluate()
            return self.others[b].evaluate_to(a_val)
        elif self.can_b:
            b_val = self.others[b].evaluate()
            return self.others[a].evaluate_to(b_val)

    def evaluate_to(self, target: int) -> int:
        """With the knowledge that this equation should result in target, propagate the info"""
        # print(f'Evaluating {self.name} to {target}')
        if self.name == 'humn': return target
        a, op, b = self.equation.split()
        if self.can_a: a_val = self.others[a].evaluate()
        if self.can_b: b_val = self.others[b].evaluate()

        match [a, op, b]:
            case [a, '+', b]:
                if self.can_a: return self.others[b].evaluate_to(target - a_val)
                elif self.can_b: return self.others[a].evaluate_to(target - b_val)
            case [a, '-', b]:
                if self.can_a: return self.others[b].evaluate_to(a_val - target)
                elif self.can_b: return self.others[a].evaluate_to(b_val + target)
            case [a, '*', b]:
                if self.can_a: return self.others[b].evaluate_to(target // a_val)
                elif self.can_b: return self.others[a].evaluate_to(target // b_val)
            case [a, '/', b]:
                if self.can_a: return self.others[b].evaluate_to(a_val // target)
                elif self.can_b: return self.others[a].evaluate_to(b_val * target)

with open('day 21/input.txt') as file:
    monkeys = {x.name: x for x in map(lambda x: Monkey(x), file.read().splitlines())}

for m in monkeys.values(): m.connect(monkeys)

#
# Puzzle 1
#
print(f'Puzzle 1 solution is: {monkeys['root'].evaluate()}')

#
# Puzzle 2
#
monkeys['root'].can_evaluate()
print(f'Puzzle 2 solution is: {monkeys['root'].force_evaluate()}')