"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    return Kth string (paragraph) that returns True
    """
    # BEGIN PROBLEM 1
    valid_paragraphs = []
    for i in paragraphs:
        if select(i):
            valid_paragraphs = valid_paragraphs + [i]
    if k > len(valid_paragraphs) - 1:
        return ""
    else:
        return valid_paragraphs[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    """return a function that returns a boolean if a paragraph contains any topic words"""
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def search(paragraph):
        paragraph = split(lower(remove_punctuation(paragraph)))
        for i in topic:
            for j in paragraph:
                if i == j:
                    return True
        return False
    return search
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    num_correct, num_typed = 0, 0
    if len(typed_words) == 0 or len(reference_words) == 0:
        return 0.0
    for i in typed_words:
        if num_typed < len(reference_words) and i == reference_words[num_typed]:
            num_correct += 1
        num_typed += 1
    return round(num_correct / len(typed_words), 4) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return len(typed) / 5 / (elapsed / 60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    closest_word = min(valid_words, key = lambda x: diff_function(user_word, x, limit))
    for i in valid_words:
        if user_word == i:
            return user_word
    if diff_function(user_word, closest_word, limit) > limit:
            return user_word
    return closest_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    small_len = min(len(goal), len(start))
    large_len = max(len(goal), len(start))
    extra_dig = large_len - small_len
    def get_letter(pos, count):
        'reached the limit'
        if count > limit:
            return limit + 1
        'reached end of string'
        if pos > small_len - 1:
            if extra_dig + count <= limit:
                return count + extra_dig
            else:
                return limit + 1
        'have not reached end of string'
        if start[pos] != goal[pos]:
            count += 1
        return get_letter(pos + 1, count)
    return get_letter(0, 0)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def next(lst):
        if len(lst) < 2:
            return [] 
        else:
            return lst[1: ]
    def get_letter(new_start, new_goal, count):
        min_dist = abs(len(new_goal) - len(new_start))
        if count > limit:
            return limit + 1
        elif new_start == new_goal:
            return count
        elif new_start == [] or new_goal == []:
            return count + min_dist
        elif new_start[0] == new_goal[0]:
            return get_letter(next(new_start), next(new_goal), count)
        else:
            'three different possibilities like count_partitions'
            add_diff = get_letter(new_start, next(new_goal), count + 1)
            remove_diff = get_letter(next(new_start), new_goal, count + 1)
            substitute_diff = get_letter(next(new_start), next(new_goal), count + 1)
            return min(add_diff, remove_diff, substitute_diff)
    return get_letter(start, goal, 0)

def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct_words = 0
    while correct_words < len(typed):
        if typed[correct_words] == prompt[correct_words]:
            correct_words += 1
        else:
            typed = []
    send({'id': user_id, 'progress': correct_words/len(prompt)})
    return correct_words/len(prompt)
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    for player in range(len(times_per_player)):
        for word in range(len(times_per_player[player])):
            if word < len(times_per_player[player]) - 1:
                times_per_player[player][word] = times_per_player[player][word + 1] - times_per_player[player][word]
            else:
                times_per_player[player].remove(times_per_player[player][word])
    return game(words, times_per_player)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    column_words = [[time(game, player, word) for player in player_indices] for word in word_indices]
    def is_lowest(value, pos):
        low = min(column_words[pos])
        if value == low:
            column_words[pos][0] = -1
            return True
        else:
            return False
    def find_low_words(row, lst):
        count, my_list = -1, []
        for col in range(len(column_words)):
            count += 1
            if is_lowest(column_words[col][row], col):
                my_list += [word_at(game, count)] 
        return my_list
    return [find_low_words(row, column_words) for row in player_indices]
    
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)