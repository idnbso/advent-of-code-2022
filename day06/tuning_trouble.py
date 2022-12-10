import sys

MARKER_SEQUENCE_LEN = 14

def main():
    fileName = sys.argv[1]
    buffers = []
    with open(fileName) as file:
        buffers = [line.strip() for line in file.readlines()]

    for buffer in buffers:
        print(get_first_marker_position(buffer))


def get_first_marker_position(buffer):
    marker_position = -1
    for position in range(len(buffer) - MARKER_SEQUENCE_LEN):
        chars_set = set()
        for characterIndex in range(position, position + MARKER_SEQUENCE_LEN):
            chars_set.add(buffer[characterIndex])

        if len(chars_set) == MARKER_SEQUENCE_LEN:
            marker_position = position + MARKER_SEQUENCE_LEN
            break
    return marker_position


if __name__ == "__main__":
    main()
