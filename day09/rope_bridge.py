import sys

DIRECTIONS_VECTORS = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}

def main():
    fileName = sys.argv[1]
    input_lines = []
    with open(fileName) as file:
        for line in file.readlines():
            input_lines.append(line.strip())

    print(get_total_visited_tail_positions(input_lines))
    specific_tail_calculator = SpecificTailCalculator(input_lines, specific_tail=9)
    print(specific_tail_calculator.get_total_visited_positions())

def get_total_visited_tail_positions(input_lines):
    head_position = (0, 0)
    tail_position = head_position
    tail_positions = set([tail_position])
    for line in input_lines:
        direction, amount = line.split(" ")
        amount = int(amount)
        for _ in range(amount):
            head_position = add_vectors(head_position, DIRECTIONS_VECTORS[direction])
            if abs(head_position[0] - tail_position[0]) > 1 or \
                abs(head_position[1] - tail_position[1]) > 1:
                x_direction = get_direction_to_add(tail_position[0], head_position[0])
                y_direction = get_direction_to_add(tail_position[1], head_position[1])
                tail_position = add_vectors(tail_position, (x_direction, y_direction))
                tail_positions.add(tail_position)

    return len(tail_positions)

class SpecificTailCalculator():
    def __init__(self, input_lines, specific_tail) -> None:
        self.input_lines = input_lines
        self.specific_tail = specific_tail
        self.head_position = (0, 0)
        self.specific_tail_positions = set()
        self.tails_positions = []

    def get_total_visited_positions(self):
        self.head_position = (0, 0)
        self.specific_tail_positions = set([self.head_position])
        self.tails_positions = [(0, 0) for _ in range(self.specific_tail)]
        for line in self.input_lines:
            direction, amount = line.split(" ")
            amount = int(amount)
            self.calculate_positions_by_movement(direction, amount)

        return len(self.specific_tail_positions)


    def calculate_positions_by_movement(self, direction, amount):
        for _ in range(amount):
            self.head_position = add_vectors(self.head_position, DIRECTIONS_VECTORS[direction])
            prev_tail_position = self.head_position
            for tail_position_idx in range(len(self.tails_positions)):
                tail_position = self.tails_positions[tail_position_idx]
                if abs(prev_tail_position[0] - tail_position[0]) > 1 or \
                    abs(prev_tail_position[1] - tail_position[1]) > 1:
                    x_direction = get_direction_to_add(tail_position[0], prev_tail_position[0])
                    y_direction = get_direction_to_add(tail_position[1], prev_tail_position[1])
                    tail_position = add_vectors(tail_position, (x_direction, y_direction))
                    self.tails_positions[tail_position_idx] = tail_position
                prev_tail_position = tail_position

            self.specific_tail_positions.add(self.tails_positions[self.specific_tail - 1])

def get_direction_to_add(n1: int, n2: int):
    diff: int = n2 - n1
    return diff // abs(diff) if diff else 0


def add_vectors(v1: tuple, v2: tuple):
    return (v1[0] + v2[0], v1[1] + v2[1])


if __name__ == "__main__":
    main()
