import sys

def main():
    fileName = sys.argv[1]
    assignmentsPairs = []
    with open(fileName) as file:
        for line in file.readlines():
            assignmentsPair = line.strip().split(',')
            assignmentsPairs.append(
                tuple(SectionAssignment(assignment) for assignment in assignmentsPair)
            )

    print(get_total_assignment_pairs_with_ranges_overlap(assignmentsPairs))


def get_total_assignment_pairs_that_fully_contain(assignmentsPairs: list):
    total = 0
    for assignmentsPair in assignmentsPairs:
        total += 1 if assignmentsPair[0].is_fully_contained(assignmentsPair[1]) \
            else 0
    return total

def get_total_assignment_pairs_with_ranges_overlap(assignmentsPairs: list):
    total = 0
    for assignmentsPair in assignmentsPairs:
        total += 1 if assignmentsPair[0].is_fully_overlap_exists(assignmentsPair[1]) \
            else 0
    return total

class SectionAssignment:
    """
    section format: "X-Y" where X, Y are integers.
    """
    def __init__(self, section: str):
        [self.min_section, self.max_section] = \
            map(lambda v: int(v), section.split('-'))

    def is_fully_contained(self, other_assignment: 'SectionAssignment'):
        return self.is_other_contained(self, other_assignment) or \
            self.is_other_contained(other_assignment, self)

    @staticmethod
    def is_other_contained(assignment: 'SectionAssignment', 
                     other_assignment: 'SectionAssignment'):
        return assignment.min_section >= other_assignment.min_section and \
            assignment.max_section <= other_assignment.max_section

    def is_fully_overlap_exists(self, other_assignment: 'SectionAssignment'):
        return self.is_overlap_exists(other_assignment) or \
            other_assignment.is_overlap_exists(self)

    def is_overlap_exists(self, other_assignment: 'SectionAssignment'):
        return self.is_in_range(self.min_section, other_assignment) or \
                self.is_in_range(self.max_section, other_assignment)

    @staticmethod
    def is_in_range(value: int, assignment: 'SectionAssignment'):
        return value >= assignment.min_section and \
            value <= assignment.max_section


if __name__ == "__main__":
    main()
