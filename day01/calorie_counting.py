import sys

def main():
    fileName = sys.argv[1]
    calories_list = []
    with open(fileName) as file:
        calories_list = [line.strip() for line in file.readlines()]

    if calories_list[-1] != '':
        calories_list.append('')

    max_calories = get_max_calories(calories_list)
    print(max_calories)

def get_max_calories(calories_list: list):
    max_calories = [0, 0, 0]
    cur = 0
    for calories in calories_list:
        if calories != '':
            cur += int(calories)
            continue

        for max_calorie_index in range(len(max_calories)):
            if cur > max_calories[max_calorie_index]:
                max_calories.insert(max_calorie_index, cur)
                max_calories.pop()
                break
        cur = 0

    return sum(max_calories)

if __name__ == "__main__":
    main()
