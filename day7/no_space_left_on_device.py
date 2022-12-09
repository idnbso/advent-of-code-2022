import sys

MAX_DIRECTORY_LARGE_SIZE = 100000
TOTAL_FILESYSTEM_SIZE = 70000000
UPDATE_INSTALLATION_SIZE = 30000000

def main():
    fileName = sys.argv[1]
    output_lines = []
    with open(fileName) as file:
        output_lines = [line.strip() for line in file.readlines()]

    calculator = DirectoriesCalculator(output_lines)
    print(calculator.get_total_size_of_largest_directories())
    print(calculator.get_smallest_directory_to_delete_for_update())

class DirectoriesCalculator:
    def __init__(self, output_lines: list):
        self.output_lines = output_lines
        self.directories_sizes = dict()
        self.directories_sizes["/"] = 0
        self.calculate_directories_sizes()

    def calculate_directories_sizes(self, cur_dir = "", line_index = 0):
        while line_index < len(self.output_lines) and \
            self.output_lines[line_index] != "$ cd ..":
            line: str = self.output_lines[line_index]
            if line.startswith("$ cd"):
                command_dir_name = line.split(" ")[-1]
                dir_name = "/" if cur_dir == "" else f'{"/" if not cur_dir else cur_dir}{command_dir_name}/'
                self.directories_sizes[dir_name] = 0
                navigation: DirectoriesCalculatorNavigation = \
                    self.calculate_directories_sizes(
                        cur_dir=dir_name,
                        line_index=line_index+1
                    )
                self.directories_sizes[cur_dir or "/"] += navigation.dir_size if cur_dir else 0
                line_index = navigation.line_index
            elif line == "$ ls":
                ls_line_index = line_index + 1
                while ls_line_index < len(self.output_lines) and \
                    not self.output_lines[ls_line_index].startswith("$"):
                    line = self.output_lines[ls_line_index]
                    if line.startswith("dir "):
                        dir_name = f'{line.split(" ")[-1]}/'
                        self.directories_sizes[f'{"/" if not cur_dir else cur_dir}{dir_name}'] = 0
                    else:
                        file_size = int(line.split(" ")[0])
                        self.directories_sizes[cur_dir] += file_size
                    ls_line_index += 1
                line_index = ls_line_index

        line_index = line_index + 1 if line_index < len(self.output_lines) and \
            self.output_lines[line_index] == "$ cd .." else line_index
        return DirectoriesCalculatorNavigation(
            cur_dir,
            self.directories_sizes[cur_dir or "/"],
            line_index
        )


    def get_total_size_of_largest_directories(self):
        total_size = 0
        for dir_name in self.directories_sizes.keys():
            if dir_name == "/": continue
            cur_size = self.directories_sizes[dir_name]
            total_size += cur_size if cur_size <= MAX_DIRECTORY_LARGE_SIZE else 0
        return total_size

    def get_smallest_directory_to_delete_for_update(self):
        used_space = self.directories_sizes["/"]
        unused_space = TOTAL_FILESYSTEM_SIZE - used_space
        min_dir_size_to_delete = list(self.directories_sizes.values())[0]
        for directory, size in self.directories_sizes.items():
            if unused_space + size >= UPDATE_INSTALLATION_SIZE and \
                size < min_dir_size_to_delete:
                min_dir_size_to_delete = size
        return min_dir_size_to_delete

class DirectoriesCalculatorNavigation:
    def __init__(self, dir_name, dir_size, line_index):
        self.dir_name  = dir_name
        self.dir_size = dir_size
        self.line_index = line_index


if __name__ == "__main__":
    main()
