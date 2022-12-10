import sys
from collections import deque

FIRST_SIGNAL_TO_CHECK = 20
SINGAL_DIFF_TO_CHECK = 40
MAX_SIGNAL_TO_CHECK = 220
MAX_SIGNAL_TO_RENDER = 240

def main():
    fileName = sys.argv[1]
    program_lines = deque()
    with open(fileName) as file:
        for line in file.readlines():
            program_lines.append(line.strip())

    print(get_sum_of_signal_strengths(program_lines.copy()))
    crt_output = get_crt_output(program_lines)
    for row in crt_output:
        print("".join(row))

def get_sum_of_signal_strengths(program_lines: deque):
    cycle = 0
    value = 1
    next_cycle_to_check = FIRST_SIGNAL_TO_CHECK
    sum_of_signal_strengths = 0
    line_index = 0
    while line_index < len(program_lines):
        cycle = line_index + 1
        line: str = program_lines[line_index]

        if cycle == next_cycle_to_check:
            sum_of_signal_strengths += value * cycle
            next_cycle_to_check += SINGAL_DIFF_TO_CHECK

        if line.startswith("addx"):
            command_value = line.split(" ")[1]
            program_lines.insert(line_index + 1, f'add {command_value}')
        elif line.startswith("add"):
            command_value = line.split(" ")[1]
            value += int(command_value)

        if cycle == MAX_SIGNAL_TO_CHECK: break
        line_index += 1

    return sum_of_signal_strengths


def get_crt_output(program_lines: deque):
    cycle = 1
    total_cycles = cycle
    line_index = 0
    sprite_position = 1
    TOTAL_OUTPUT_ROWS = 6
    TOTAL_OUTPUT_ROW_PIXELS = 40
    output_matrix = [['.' for _ in range(TOTAL_OUTPUT_ROW_PIXELS)] \
        for _ in range(TOTAL_OUTPUT_ROWS)]
    while line_index < len(program_lines):
        line: str = program_lines[line_index]

        if cycle >= sprite_position and cycle <= sprite_position + 2:
            row = total_cycles // TOTAL_OUTPUT_ROW_PIXELS
            col = cycle % TOTAL_OUTPUT_ROW_PIXELS
            output_matrix[row][col - 1] = "#"

        if line.startswith("addx"):
            program_lines[line_index] = line.replace("addx", "add")
        elif line.startswith("add"):
            sprite_position = (sprite_position + int(line.split(" ")[1]))
        
        if not line.startswith("addx"):
            line_index += 1

        cycle = (cycle + 1) % TOTAL_OUTPUT_ROW_PIXELS
        total_cycles += 1

    return output_matrix

if __name__ == "__main__":
    main()
