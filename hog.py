"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact
GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice = six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sod = False
    total_rolled = 1
    dice_total = 0 
    while total_rolled <= num_rolls:
        outcome = dice()
        if outcome == 1:
            sod = True
        total_rolled += 1
        dice_total = dice_total + outcome
    if sod == True:
        return 1
    else:
        return dice_total        
    # END PROBLEM 1
# print("test roll_dice")
# fixed_dice = make_test_dice(2,4,2,2)
# print(roll_dice(4,fixed_dice))

def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    """find tens digit of opponets score"""
    tens_digit = opponent_score // 10 
    if tens_digit > 9:
        tens_digit = tens_digit % 10 
    """find ones digit of current players score"""
    if player_score > 9:
        ones_digit = player_score % 10
    else: 
        ones_digit = player_score
    boar_score = 3 * abs(tens_digit - ones_digit)
    if boar_score > 1:
        return boar_score
    else: 
        return 1        
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        score = boar_brawl(player_score, opponent_score)
    else:
        score = roll_dice(num_rolls, dice)
    return score
    # END PROBLEM 3
# print("take turn: answer should be 30")
# fixed_dice = make_test_dice(2,4,6)
# print(take_turn(1, 21, 46,fixed_dice))


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""
    # BEGIN PROBLEM 4
    num = 1 
    factors = 0 
    while num <= n:
        if n % num == 0:
            factors += 1
        num += 1 
    return factors 
# print("test num_factors")
# print(num_factors(5))        
    # END PROBLEM 4

def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    # BEGIN PROBLEM 4
    if num_factors(score) == 3 or num_factors(score) == 4:
        while is_prime(score) == False:
            score += 1
    return score
# print("test sus_points")
# print(sus_points(67))
    # END PROBLEM 4

def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    # BEGIN PROBLEM 4
    score = take_turn(num_rolls, player_score, opponent_score, dice) + player_score
    return sus_points(score)
    # END PROBLEM 4
# print("testing sus update: expected 67")
# fixed_dice = make_test_dice(3,3,3,3,6)
# print(sus_update(5, 49, 46, fixed_dice))

def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal or score1 < goal:
        if who == 0:
            score0 = update(strategy0(score0, score1), score0, score1, dice)
            
        else:
            num_rolls = strategy1
            score1 = update(strategy1(score1, score0), score1, score0, dice)
        who = 1 - who
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    def strategy_function(player_score, opponet_score):
        return n 
    return strategy_function
    always_roll_5 = always_roll(5)
    always_roll_7 = always_roll(7)

    # END PROBLEM 6
    


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    initial_roll = None
    for player_score in range(goal):
        for opponet_score in range(goal):
            current_role = strategy(player_score, opponet_score)
            if initial_roll == None:
                initial_roll = current_role 
            elif initial_roll != current_role:
                return False
    return True
    # END PROBLEM 7
print("testing is_always: expecting True")
print(is_always_roll(catch_up))


def make_averaged(original_function, samples_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called SAMPLES_COUNT times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    def averaged(*args):
        result = 0 
        for i in range(samples_count):
            result += original_function(*args)
        return result/samples_count
    return averaged
print("testing make_averaged: expecting 3.0")
dice1 = make_test_dice(4, 2, 5, 1)  
averaged_dice = make_averaged(roll_dice, 40)
print(averaged_dice(1,dice1))
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, samples_count=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    max_average = 0
    amount_of_rolls = 1
    for num_rolls in range(1,11):
        average_roll_dice = make_averaged(roll_dice, samples_count)
        average_score = average_roll_dice(num_rolls, dice)
        if average_score > max_average:
            max_average = average_score
            amount_of_rolls = num_rolls
        elif average_score == max_average:
            max_average = min(average_score,max_average)
    return amount_of_rolls

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    if boar_brawl(score,opponent_score) >= threshold:
        return 0
    else:
        return num_rolls
print("testing boar_strategy: expecting to return 0")
print(boar_strategy(29, 16))
print("testing boar strategy: expecting to return 6")
print(boar_strategy(23,28))

def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    if sus_update(num_rolls, score, opponent_score) - score > threshold:
        return 0
    else:
        return num_rolls  
print("testing sus_strategy: expecting 0")
print(sus_strategy(53,60))


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()