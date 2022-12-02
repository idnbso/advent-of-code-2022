import sys

SHAPES = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}

WINNING_PLAYS = {
    'X': 'C',
    'Y': 'A',
    'Z': 'B'
}

OPPONRNT_WINNING_PLAYS = {
    'B': 'X',
    'C': 'Y',
    'A': 'Z'
}

OPPONRNT_LOSING_PLAYS = {
    'C': 'X',
    'A': 'Y',
    'B': 'Z'
}

SHAPE_SCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

LOST_SCORE = 0
DRAW_SCORE = 3
WIN_SCORE = 6

STRATEGY_SCORE = {
    'X': LOST_SCORE,
    'Y': DRAW_SCORE,
    'Z': WIN_SCORE
}

def main():
    fileName = sys.argv[1]
    guide = []
    with open(fileName) as file:
        guide = [line.strip() for line in file.readlines()]

    print(get_total_score_by_guide(guide))

def get_total_score_by_guide_naive(guide: list):
    total_score = 0
    for round in guide:
        opponent_play = round[0]
        player_play = round[2]
        total_score += SHAPE_SCORES[player_play]
        if SHAPES[opponent_play] == player_play:
            total_score += DRAW_SCORE
        elif opponent_play == WINNING_PLAYS[player_play]:
            total_score += WIN_SCORE
        else:
            total_score += LOST_SCORE

    return total_score

def get_total_score_by_guide(guide: list):
    total_score = 0
    for round in guide:
        opponent_play = round[0]
        strategy_play = round[2]
        player_play = None
        if STRATEGY_SCORE[strategy_play] == WIN_SCORE:
            player_play = OPPONRNT_LOSING_PLAYS[opponent_play]
            total_score += WIN_SCORE
        elif STRATEGY_SCORE[strategy_play] == LOST_SCORE:
            player_play = OPPONRNT_WINNING_PLAYS[opponent_play]
            total_score += LOST_SCORE
        else:
            player_play = SHAPES[opponent_play]
            total_score += DRAW_SCORE

        total_score += SHAPE_SCORES[player_play]

    return total_score

if __name__ == "__main__":
    main()
