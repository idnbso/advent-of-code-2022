import sys
import math

STARTING_POSITION = 'S'
BEST_SIGNAL_POSITION = 'E'
HIGHEST_ELEVATION = 'z'

DIRECTIONS = [
    (0, 1), # Up
    (1, 0), # Right
    (-1, 0), # Left
    (0, -1), # Down
]

def main():
    fileName = sys.argv[1]
    input_lines = []
    with open(fileName) as file:
        input_lines = [line.strip() for line in file.readlines()]

    heightmap = Heightmap(input_lines)
    print(heightmap.get_shortest_path_to_best_signal())

    #heightmap.print_heightmap()
    pass


class Heightmap:
    def __init__(self, input_lines: list) -> None:
        self.total_rows = len(input_lines)
        self.total_cols = len(input_lines[0])
        self.total_vertices = self.total_rows * self.total_cols
        self.visited = dict()
        self.map = []
        for line in input_lines:
            self.map.append([char for char in line])

        self.starting_position = self.get_position(STARTING_POSITION)
        self.ending_position = self.get_position(HIGHEST_ELEVATION)
        (start_row, start_col) = self.starting_position
        self.start_row = start_row
        self.start_col = start_col
        (end_row, end_col) = self.ending_position
        self.end_row = end_row
        self.end_col = end_col
        self.map[start_row][start_col] = 'a'
        self.map[end_row][end_col] = 'z'

        self.adjacency_list = dict()

        for row in range(self.total_rows):
            for col in range(self.total_cols):
                self.adjacency_list[(row, col)] = []

                for direction in DIRECTIONS:
                    d_row = row + direction[0]
                    d_col = col + direction[1]

                    if self.is_position_invalid(d_row, d_col) or \
                        ord(self.map[d_row][d_col]) - ord(self.map[row][col]) >= 2:
                        continue

                    self.adjacency_list[(row, col)].append((d_row, d_col))


    def get_shortest_path_to_best_signal(self) -> int:
        predecessors = [[0 for _ in range(self.total_cols)] for _ in range(self.total_rows)]
        distances = [[0 for _ in range(self.total_cols)] for _ in range(self.total_rows)]
  
        if (self.bfs(predecessors, distances) == False):
            print("Given source and destination are not connected")
    
        path = []
        crawl = self.ending_position
        path.append(crawl)
        
        while (predecessors[crawl[0]][crawl[1]] != -1):
            path.append(predecessors[crawl[0]][crawl[1]])
            crawl = predecessors[crawl[0]][crawl[1]]

        return distances[self.end_row][self.end_col]


    def bfs(self, predecessors, distances):
        # initialize search state
        queue = []
        visited = [[False for _ in range(self.total_cols)] for _ in range(self.total_rows)]

        for row in range(self.total_rows):
            for col in range(self.total_cols):
                distances[row][col] = math.inf
                predecessors[row][col] = -1
        
        # handle source vertex
        visited[self.start_row][self.start_col] = True
        distances[self.start_row][self.start_col] = 1
        queue.append((self.start_row, self.start_col))

        # breadth first search
        while (len(queue) != 0):
            u: tuple = queue[0]
            queue.pop(0)

            for i in range(len(self.adjacency_list[u])):
                current = self.adjacency_list[u][i]
                (row, col) = current
                if (visited[row][col] == False):
                    visited[row][col] = True
                    distances[row][col] = distances[u[0]][u[1]] + 1
                    predecessors[row][col] = u
                    queue.append((row, col))
    
                    if ((row, col) == (self.end_row, self.end_col)):
                        return True
  
        return False


    def is_position_invalid(self, row, col) -> bool:
        return self.is_row_out_of_bounds(row) or \
            self.is_col_out_of_bounds(col)


    def is_row_out_of_bounds(self, row) -> bool:
        return row < 0 or row >= self.total_rows

    
    def is_col_out_of_bounds(self, col) -> bool:
        return col < 0 or col >= self.total_cols

    
    def get_position(self, value) -> tuple:
        for row in range(self.total_rows):
            for col in range(self.total_cols):
                if self.map[row][col] == value:
                    return (row, col)


    def print_heightmap(self) -> None:
        for row in range(self.total_rows):
            for col in range(self.total_cols):
                if (row, col) in self.visited and \
                    self.visited[(row, col)] != -1:
                    print(f'{self.visited[(row, col)]} '.rjust(4, '0'), end='')
                else:
                    print('000 ', end='')
            print()


if __name__ == "__main__":
    main()
