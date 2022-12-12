import sys
from functools import reduce
import copy
import math

BORED_MONKEY_DIVISION_VALUE = 3
MAX_PLAY_ROUND_TO_CHECK = 10_000

def main() -> None:
    fileName = sys.argv[1]
    monkies_data = dict()
    with open(fileName) as file:
        monkey_data_lines = []
        lines = file.readlines()
        for line_index in range(len(lines) + 1):
            line_data = lines[line_index].strip() \
                if line_index < len(lines) else None
            if not line_data:
                monkey_data = MonkeyData(monkey_data_lines)
                monkies_data[monkey_data.id] = monkey_data
                monkey_data_lines = []
                continue
            monkey_data_lines.append(line_data)
    

    print(get_monkey_business_level(copy.deepcopy(monkies_data)))


def get_monkey_business_level(monkies_data: dict, max_round = MAX_PLAY_ROUND_TO_CHECK):
    divisors = map(lambda m: m.test.divisor, monkies_data.values())
    divisors_mul = reduce(lambda all, v: math.lcm(all, v), divisors)
    for _ in range(max_round):
        for monkey_id in range(len(monkies_data)):
            monkey_data: MonkeyData = monkies_data[monkey_id]
            monkey_data.play_round(monkies_data, divisors_mul)

    max_inspections = [0, 0]
    for monkey_data in monkies_data.values():
        for max_inspection_index in range(len(max_inspections)):
            max_inspection = max_inspections[max_inspection_index]
            if monkey_data.total_inspected_items > max_inspection:
                max_inspections.insert(max_inspection_index, monkey_data.total_inspected_items)
                max_inspections.pop()
                break

    return reduce(lambda i1, i2: i1 * i2, max_inspections)


class MonkeyData:
    def __init__(self, data_lines: list) -> None:
        self.id = int(data_lines[0].split(":")[0].split(" ")[1])
        self.total_inspected_items = 0

        startup_items = data_lines[1].split(":")[1].strip()
        self.startup_items = list(map(lambda item: int(item), \
            startup_items.split(",")))

        self.operation = data_lines[2].split(" = ")[1]

        test = data_lines[3].split(":")[1].strip()
        divisor = int(test.split(" ")[-1])
        if_true_monkey_id = int(data_lines[4].split(":")[1].strip().split(" ")[-1])
        if_false_monkey_id = int(data_lines[5].split(":")[1].strip().split(" ")[-1])
        self.test = MonkeyDataTest(divisor, if_true_monkey_id, if_false_monkey_id)


    def play_round(self, monkies_data: dict, divisors_mul: int):
        for worry_level in self.startup_items:
            to_eval = self.operation.replace("old", str(worry_level))

            new_worry_level = eval(to_eval) % divisors_mul
            # new_worry_level //= BORED_MONKEY_DIVISION_VALUE
            
            next_monkey_id = self.test.get_monkey_id_by_worry_level(new_worry_level)
            next_monkey_data: MonkeyData = monkies_data[next_monkey_id]
            next_monkey_data.startup_items.append(new_worry_level)
            self.total_inspected_items += 1
        self.startup_items = []

class MonkeyDataTest:
    def __init__(self, divisor, \
        if_true_monkey_id, if_false_monkey_id) -> None:
        self.divisor = divisor
        self.if_true_monkey_id = if_true_monkey_id
        self.if_false_monkey_id = if_false_monkey_id

    def get_monkey_id_by_worry_level(self, worry_level):
        return self.if_true_monkey_id if \
            worry_level % self.divisor == 0 else \
                self.if_false_monkey_id


if __name__ == "__main__":
    main()
