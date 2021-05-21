
import random

from yatzy import *


def play_yatzy():
    """
    Play an interactive game of Yatzy on the command line
    """
    available_categories = [yatzy, full_house, four_of_a_kind, three_of_a_kind, two_pairs,
                            small_straight, large_straight,
                            ones, twos, threes, fours, fives, sixes,
                            chance]
    play_yatzy_with_categories(available_categories)


def play_yatzy_with_categories(available_categories, input_source=input):
    """
    Play an interactive game of Yatzy on the command line,
    with only the given categories available

    :param available_categories: list of category functions.
    Each function takes a list of dice integers, and returns an integer score

    """
    scored_categories = []
    total_score = 0
    while len(available_categories) > 0:
        dice = do_dice_rolling(input_source)
        category = do_category_choice(available_categories, dice, input_source)

        available_categories.remove(category)
        score = category(dice)
        scored_categories.append((category, score))
        total_score += score
        print(f"Your score is now {total_score}")
    print(scorecard(scored_categories))
    print(f"Final Score: {total_score}")


class StubInput:
    """
    This class is used by the tests to supply user input
    """
    def __init__(self, return_values):
        self.return_value_list = return_values
        self.counter = 0

    def __call__(self, *args, **kwargs):
        value = self.return_value_list[self.counter]
        self.counter += 1
        return value


def do_dice_rolling(input_source=input):
    """
    Interactive command-line dice rolling.
    Roll 5 dice and present them to the user. Allow the user to re-roll up to twice.

    :return: the final 5 dice that were rolled

    >>> random.seed(1234)
    >>> do_dice_rolling(_reroll_nothing)
    Your roll is:
    [1, 1, 1, 4, 5]
    [1, 1, 1, 4, 5]
    [1, 1, 1, 4, 5]
    [1, 1, 1, 4, 5]
    >>> do_dice_rolling(_reroll_everything)
    Your roll is:
    [1, 1, 1, 6, 6]
    [1, 1, 2, 3, 6]
    [1, 1, 1, 1, 3]
    [1, 1, 1, 1, 3]
    """
    print("Your roll is:")
    dice = roll()
    print(dice)
    re_rolls_left = 2
    while re_rolls_left:
        try:
            to_re_roll = input_source("Which dice will you re-roll?\n")
            new_dice = re_roll(dice[:], convert_input_to_dice(to_re_roll))
        except ValueError:
            print("invalid re-roll choice. Please enter a comma separated list of dice eg 1,2")
            continue
        print(new_dice)
        re_rolls_left -= 1
        dice = new_dice
    return dice


def _reroll_nothing(*args, **kwargs):
    return ""


def _reroll_everything(*args, **kwargs):
    return "1,2,3,4,5,6"


def do_category_choice(available_categories, dice, input_source=input):
    """
    Ask the player to interactively choose a scoring category, on the command-line.

    :param available_categories: the categories available for the player to choose from
    :param dice: the dice the player previously rolled
    :return: the category chosen by the player, to score the dice in.

    >>> do_category_choice([ones, twos], [1,1,1,2,2], _choose_ones) #doctest: +ELLIPSIS
    Hint: available categories and scores:
    [(4, 'twos'), (3, 'ones')]
    <function ones at 0x...>

    """
    print("Hint: available categories and scores:")
    potential_scores = scores_in_categories(dice, available_categories)
    print([(score, fn.__name__) for score, fn in potential_scores])
    category = None
    while category not in available_categories:
        chosen_category = input_source("Which category would you like to score this roll in?\n")
        try:
            category_index = [fn.__name__ for fn in available_categories].index(chosen_category)
            category = available_categories[category_index]
        except ValueError:
            print("invalid category choice. Please enter a category name from the list shown above")
    return category


def _choose_ones(*args, **kwargs):
    return "ones"


def convert_input_to_dice(to_re_roll):
    """
    Parse the user intput into a list of dice

    :param to_re_roll: the raw comma-separated string received from the user input
    :return: a list of dice which are integers

    >>> convert_input_to_dice("1")
    [1]
    >>> convert_input_to_dice("1,2")
    [1, 2]
    >>> convert_input_to_dice("")
    []
    >>> convert_input_to_dice("foobar")
    Traceback (most recent call last):
    ...
    ValueError: invalid literal for int() with base 10: 'foobar'

    """
    if to_re_roll:
        dice = [int(d) for d in to_re_roll.split(",")]
        return [die for die in dice if die in (1, 2, 3, 4, 5, 6)]
    return []


def roll(number_of_dice=5):
    """
    Roll the indicated number of 6 sided dice using a random number generator
    :param number_of_dice: how many dice to roll
    :return: a list containing the rolled numbers

    >>> random.seed(1234)
    >>> roll()
    [1, 1, 1, 4, 5]
    >>> roll()
    [1, 1, 1, 6, 6]
    >>> roll()
    [1, 1, 1, 2, 3]
    >>> roll()
    [3, 4, 5, 5, 6]
    >>> roll()
    [1, 2, 2, 4, 6]

    """
    return sorted(random.choice((1, 2, 3, 4, 5, 6)) for i in range(number_of_dice))


def re_roll(dice, dice_to_re_roll):
    """
    Re-roll zero or more dice from the original roll. Ignores requests to re-roll dice that were not present in original roll.

    :param dice: the original roll
    :param dice_to_re_roll: the dice you wish you re-roll
    :return: the new dice roll

    >>> random.seed(1234)
    >>> re_roll([1,2,3,4,5], [1])
    [2, 3, 4, 4, 5]
    >>> re_roll([1,2,3,4,5], [1,2])
    [1, 1, 3, 4, 5]
    >>> re_roll([1,2,3,4,5], [])
    [1, 2, 3, 4, 5]
    >>> re_roll([1,2,3,4,5], [1,2,3,4,5])
    [1, 1, 5, 6, 6]
    >>> re_roll([1,1,1,1,1], [2])
    [1, 1, 1, 1, 1]

    """
    original_dice_length = len(dice)
    [dice.remove(die) for die in dice_to_re_roll if die in dice]
    new_rolls = roll(original_dice_length-len(dice))
    dice.extend(new_rolls)
    return sorted(dice)


def scorecard(scored_categories):
    """
    Print a scorecard showing what the player has scored in each category

    :param scored_categories: a list of tuples (category, score)
    :return: a string containing the scorecard, highest scores first

    >>> scorecard([(ones, 3), (twos, 6)]).splitlines()
    ['twos:       6', 'ones:       3']

    """
    sorted_scores = sorted(scored_categories, reverse=True, key=itemgetter(1))
    result = ""
    for (category, score) in sorted_scores:
        result += f"{category.__name__}:       {score}\n"
    return result


if __name__ == "__main__":
    play_yatzy()
