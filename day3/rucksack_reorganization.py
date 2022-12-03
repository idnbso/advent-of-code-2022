import sys

def main():
    fileName = sys.argv[1]
    rucksacks = []
    with open(fileName) as file:
        rucksacks = [line.strip() for line in file.readlines()]

    print(get_sum_of_badges_priorities(rucksacks))

def get_sum_of_items_priorities(rucksacks: list):
    sum_of_priorities = 0
    for rucksack in rucksacks:
        first_compartment_set = set()

        for itemIndex in range(len(rucksack) // 2):
            first_compartment_set.add(rucksack[itemIndex])

        for itemIndex in range(len(rucksack) // 2, len(rucksack)):
            if rucksack[itemIndex] in first_compartment_set:
                sum_of_priorities += get_item_priority(rucksack[itemIndex])
                break

    return sum_of_priorities

def get_sum_of_badges_priorities(rucksacks: list):
    TOTAL_ELVES_TO_CHECK = 3
    sum_of_priorities = 0

    group_set = set()
    for rucksackIndex in range(len(rucksacks) + 1):
        if rucksackIndex % TOTAL_ELVES_TO_CHECK == 0:
            for item in group_set:
                sum_of_priorities += get_item_priority(item)

            if rucksackIndex >= len(rucksacks):
                break

            group_set = set(list(rucksacks[rucksackIndex]))
            continue

        common_set = set()
        for item in rucksacks[rucksackIndex]:
            if item in group_set:
                common_set.add(item)

        group_set = common_set

    return sum_of_priorities

def get_item_priority(item: str):
    if item >= 'a' and item <= 'z':
        return ord(item) - ord('a') + 1
    elif item >= 'A' and item <= 'Z':
        return ord(item) - ord('A') + 27
    raise ValueError('Item can only be a lower-case or upper-case english character.')

if __name__ == "__main__":
    main()
