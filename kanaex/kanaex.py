"""

"""
import os
import re
import sys
import yaml
import shutil
import random

PATH = os.path.dirname(os.path.abspath(__file__))
COLUMN_SIZE = shutil.get_terminal_size().columns

class UserError(Exception):
    pass


class Kanaex:
    hiragana = 'あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなに' + \
        'ぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん'
    katakana = 'アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニ' + \
        'ヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヲン'
    romaji = ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko', \
            'ga', 'gi', 'gu', 'ge', 'go', 'sa', 'shi', 'su', 'se', 'so', \
            'za', 'ji', 'zu', 'ze', 'zo', 'ta', 'chi', 'tsu', 'te', 'to', \
            'da', 'ji', 'zu', 'de', 'do', 'na', 'ni', 'nu', 'ne', 'no', \
            'ha', 'hi', 'fu', 'he', 'ho', 'ba', 'bi', 'bu', 'be', 'bo', \
            'pa', 'pi', 'pu', 'pe', 'po', 'ma', 'mi', 'mu', 'me', 'mo', \
            'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'n']

    def __init__(self, name):
        if not name.isalnum():
            raise UserError('Names can only consist letters and numbers')
        self.name = name
        self.stats = None

    def __str__(self):
        s = f'Player: {self.name} \n'
        if self.stats['game_count'] != 0:
            s += f"Played {self.stats['game_count']} games with \
                %{self.stats['success_rate']} success rate."
        else:
            s += 'There is no stats yet!'
        return s

    def create_yaml(self):
        dict = {'name': self.name,
            'stats': {'game_count': 0, 'success_rate': 0},
            'played': []}
        self.stats = dict
        with open(os.path.join(PATH, f'{self.name}.yaml'), 'w') as stats_file:
            yaml.dump(dict, stats_file)

    def update_stats(self, success_rate):
        self.stats['game_count'] += 1
        self.stats['success_rate'] = float(
            f"{(self.stats['success_rate']*(self.stats['game_count']-1)+success_rate)/self.stats['game_count']:.2f}")
        with open(os.path.join(PATH, f'{self.name}.yaml'), 'r') as stats_file:
            stats_yaml = yaml.load(stats_file, Loader=yaml.SafeLoader)
            stats_yaml['stats'] = self.stats
            stats_yaml['played'].append(success_rate)
        with open(os.path.join(PATH, f'{self.name}.yaml'), 'w') as stats_file:
            yaml.dump(stats_yaml, stats_file)

    def play(self, char_list):
        true_count = 0
        for round in range(len(char_list)):
            print(f'{true_count} correct out of {round}')
            print(('\u001b[31m' + char_list[round] + '\u001b[0m').center(COLUMN_SIZE))
            ans = input(COLUMN_SIZE//4*' ')
            try:
                char_index = Kanaex.hiragana.index(char_list[round])
            except ValueError:
                char_index = Kanaex.katakana.index(char_list[round])
            if Kanaex.romaji[char_index] == ans:
                true_count += 1
            print('\033[3A\033[J')
        success_rate = float(f'{true_count/len(char_list)*100:.2f}')
        print(f'Congrats {self.name}, your success rate for this game was %{success_rate}')
        self.update_stats(success_rate)

    @staticmethod
    def mode_selector(mode_input):
        if mode_input.lower() in ['h', 'hira', 'hiragana']:
            return Kanaex.hiragana
        elif mode_input.lower() in ['k', 'kata', 'katakana']:
            return Kanaex.katakana
        elif mode_input.lower() in ['b', 'both']:
            return Kanaex.hiragana + Kanaex.katakana
        else:
            raise UserError(f'No mode found: \'{mode_input}\'')

if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = input('Enter a name to start:\n')
    # Initial statements...
    # Looks up script folder for yaml files and if their names are alphanumeric
    # or not; else gets input from user to create a new player file.
    if not [file.split('.yaml')[0] for file in os.listdir(PATH) if file.endswith('.yaml') and file.split('.yaml')[0].isalnum()]:
        print('There is no players found.\n')
        Kanaex.create_yaml(Kanaex(name))
        print(f'\nCreated player {name}')

    # Greeting/Loading
    player = Kanaex(name)
    with open(os.path.join(PATH, f'{player.name}.yaml'), 'r') as stats_file:
        player.stats = yaml.load(stats_file, Loader=yaml.SafeLoader)['stats']

    print('Playing as ' + str(player))

    # Game Screen
    while True:
        mode_input = input('Select game mode: \n \
            [H, hira, hiragana] [K, kata, katakana] [B, both]\n->  ')
        char_list = list(Kanaex.mode_selector(mode_input))
        random.shuffle(char_list)
        player.play(char_list)

        play_again = input('Do you want to play again? [y/N]')
        if play_again.lower() not in ['y', 'yes']:
            print('See you soon...')
            break
