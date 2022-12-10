import sys

def main():
    fileName = sys.argv[1]
    trees_heights_map = []
    with open(fileName) as file:
        trees_heights_map = [[int(digit) for digit in line.strip()] for line in file.readlines()]
    
    print(get_total_visible_trees(trees_heights_map))
    print(get_highest_scenic_score(trees_heights_map))

def get_total_visible_trees(trees_heights_map):
    (max_top_heights_map, max_bottom_heights_map, max_left_heights_map, max_right_heights_map) = \
        get_max_heights_maps(trees_heights_map)
    total_visible_trees = 0
    total_rows = len(trees_heights_map)
    total_cols = len(trees_heights_map[0])
    for row in range(1, total_rows - 1):
        for col in range(1, total_cols - 1):
            if trees_heights_map[row][col] > max_top_heights_map[row - 1][col] or \
                trees_heights_map[row][col] > max_bottom_heights_map[row + 1][col] or \
                trees_heights_map[row][col] > max_right_heights_map[row][col + 1] or \
                trees_heights_map[row][col] > max_left_heights_map[row][col - 1]:
                total_visible_trees += 1

    bottom_and_top_cells = total_cols * 2
    sides_cells = 2 * (total_rows - 2)
    total_visible_trees += bottom_and_top_cells + sides_cells
    return total_visible_trees


def get_max_heights_maps(heights_map):
    total_rows = len(heights_map)
    total_cols = len(heights_map[0])
    max_top_heights_map = [[heights_map[row][col] for col in range(total_cols)] for row in range(total_rows)]
    max_bottom_heights_map = [[heights_map[row][col] for col in range(total_cols)] for row in range(total_rows)]
    max_left_heights_map = [[heights_map[row][col] for col in range(total_cols)] for row in range(total_rows)]
    max_right_heights_map = [[heights_map[row][col] for col in range(total_cols)] for row in range(total_rows)]

    for row in range(1, total_rows - 1):
        for col in range(1, total_cols - 1):
            top_cell = max_top_heights_map[row - 1][col]
            cell = max_top_heights_map[row][col]
            max_top_heights_map[row][col] = max(cell, top_cell)

    for row in range(total_rows - 2, 0, -1):
        for col in range(1, total_cols - 1):
            bottom_cell = max_bottom_heights_map[row + 1][col]
            cell = max_bottom_heights_map[row][col]
            max_bottom_heights_map[row][col] = max(cell, bottom_cell)

    for row in range(1, total_rows - 1):
        for col in range(1, total_cols - 1):
            left_cell = max_left_heights_map[row][col - 1]
            cell = max_left_heights_map[row][col]
            max_left_heights_map[row][col] = max(cell, left_cell)

    for row in range(1, total_rows - 1):
        for col in range(total_cols - 2, 0, -1):
            right_cell = max_right_heights_map[row][col + 1]
            cell = max_right_heights_map[row][col]
            max_right_heights_map[row][col] = max(cell, right_cell)

    return (
        max_top_heights_map,
        max_bottom_heights_map,
        max_left_heights_map,
        max_right_heights_map
    )


def get_highest_scenic_score(trees_heights_map):
    highest_scenic_score = 0
    for row in range(len(trees_heights_map)):
        for col in range(len(trees_heights_map[0])):
            score = get_cell_scenic_score(trees_heights_map, row, col)
            highest_scenic_score = score if score > highest_scenic_score \
                else highest_scenic_score

    return highest_scenic_score

def get_cell_scenic_score(trees_heights_map, row_idx, col_idx):
    total_rows = len(trees_heights_map)
    total_cols = len(trees_heights_map[0])
    cell = trees_heights_map[row_idx][col_idx]

    left_score = 0
    for cur_col_idx in range(col_idx - 1, -1, -1):
        left_score += 1
        if cur_col_idx == 0 or \
            trees_heights_map[row_idx][cur_col_idx] >= cell:
            break
    
    right_score = 0
    for cur_col_idx in range(col_idx + 1, total_cols):
        right_score += 1
        if cur_col_idx == total_cols or \
            trees_heights_map[row_idx][cur_col_idx] >= cell:
            break

    top_side = 0
    for cur_row_idx in range(row_idx - 1, -1, -1):
        top_side += 1
        if cur_row_idx == 0 or \
            trees_heights_map[cur_row_idx][col_idx] >= cell:
            break

    bottom_side = 0
    for cur_row_idx in range(row_idx + 1, total_rows):
        bottom_side += 1
        if cur_row_idx == total_rows or \
            trees_heights_map[cur_row_idx][col_idx] >= cell:
            break

    return top_side * bottom_side * right_score * left_score


if __name__ == "__main__":
    main()
