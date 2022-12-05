import sys

def main():
    fileName = sys.argv[1]
    stacks = []
    moves = []
    moves_line_start = -1
    with open(fileName) as file:
        file_lines = file.readlines()
        stacks, line_counter = parse_stacks(file_lines)
        moves_line_start = line_counter + 2
        moves = parse_moves(file_lines, moves_line_start)

    for moveIndex in range(len(moves)):
        move: ArrangementMove = moves[moveIndex]
        move.execute(stacks)

    message = ''
    for stackIndex in range(len(stacks)):
        stack: list = stacks[stackIndex]
        message += stack.pop()

    print(message)


def parse_stacks(file_lines: list):
    stacks = []
    line_counter = 0
    total_stacks = 0
    for file_line in file_lines:
        line: str = file_line.strip()
        if line[0] == '1':
            total_stacks = int(line[-1])
            break
        line_counter += 1

    for _ in range(total_stacks):
        stacks.append(list())

    for line_index in range(line_counter - 1, -1, -1):
        crates: str = file_lines[line_index]
        for stack_index in range(total_stacks):
            crate_letter = crates[1 + stack_index*4]
            if crate_letter == ' ': continue
            stack: list = stacks[stack_index]
            stack.append(crate_letter)

    return (stacks, line_counter)


def parse_moves(file_lines, moves_line_start):
    moves = []
    for line_index in range(moves_line_start, len(file_lines)):
        procedure_step = file_lines[line_index]
        moves.append(ArrangementMove(procedure_step))
    return moves


class ArrangementMove:
    def __init__(self, procedure_step: str):
        parts = procedure_step.split(' ')
        self.amount = int(parts[1])
        self.fromStackId = int(parts[3])
        self.toStackId = int(parts[5])

    def execute(self, stacks: list):
        fromStack: list = stacks[self.fromStackId - 1]
        toStack: list = stacks[self.toStackId - 1]
        for crateIndex in range(self.amount):
            crate = fromStack.pop(-self.amount + crateIndex)
            toStack.append(crate)

    def execute_as_stack(self, stacks: list):
        fromStack: list = stacks[self.fromStackId - 1]
        toStack: list = stacks[self.toStackId - 1]
        for _ in range(self.amount):
            crate = fromStack.pop()
            toStack.append(crate)


if __name__ == "__main__":
    main()
