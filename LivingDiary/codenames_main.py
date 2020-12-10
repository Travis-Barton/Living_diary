from codenames_bot import guesser
from codenames_plotter import plot_field
import os
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')
os.chdir('/Users/tbarton/Documents/GitHub/Living_diary/LivingDiary')
text = pd.read_csv('words.txt', header=None)
# selecting game_in_func
game = text.sample(25)
# organaizing game_in_func
game.loc[:, 'label'] = ['red' for i in range(8)] + ['blue' for i in range(9)] + ['black'] + ['grey' for i in range(7)]
game.columns = ['word', 'label']
game.loc[:, 'vector'] = [[nlp(word).vector] for word in game.word.tolist()]
game.index = game.word.values
game.to_csv('game_in_func.csv')
def play_game(game_in_func, start='blue'):
    game_in_func = pd.read_csv('game_in_func.csv', index_col=0)
    game_in_func_dictionary = {}
    for row in game_in_func.iterrows():
        row = row[1]
        if row['label'] == 'black':
            game_in_func_dictionary[row['word']] = 4  # 2
        elif row['label'] == 'red':
            game_in_func_dictionary[row['word']] = 0  # 0
        elif row['label'] == 'blue':
            game_in_func_dictionary[row['word']] = 1  # 0
        elif row['label'] == 'grey':
            game_in_func_dictionary[row['word']] = 2  # 2
    # print(game_in_func_dictionary)
    while((len(game_in_func.loc[game_in_func['label'] == 'red']) != 0) or (len(game_in_func.loc[game_in_func['label'] == 'blue']) != 0)):
        # print(game_in_func_dictionary)
        plot_field(game_in_func_dictionary, colors=None)
        # print(game_in_func.loc[game_in_func['label'] != 'chosen', ['word', 'label']])
        team = start
        print(f'{team} is up')
        hint = input('what is your hint?: ')
        number = int(input('what is your number?: '))
        guess = guesser(hint, number, game_in_func.loc[game_in_func['label'] != 'chosen'].word.tolist())
        print(f'my guess(s) is (are) {guess}')
        for g in guess:
            if g == game_in_func.loc[game_in_func['label'] == 'black'].values[0][0]:
                print(f'{team} picked the assasin!!!')
                if team == 'blue':
                    return 'red'
                else:
                    return 'blue'
            elif g in game_in_func.loc[game_in_func['label'] == team, 'word'].tolist():
                game_in_func.loc[g, 'label'] = 'chosen'
                game_in_func.to_csv('game_in_func.csv')
            elif g in game_in_func.loc[:, 'word'].tolist():
                game_in_func.loc[g, 'label'] = 'chosen'
                game_in_func.to_csv('game_in_func.csv')
                break
            else:
                break
        if (len(game_in_func.loc[game_in_func['label'] == 'red']) == 0):
            print('red wins!!!!')
            return 'red'
        if len(game_in_func.loc[game_in_func['label'] == 'blue']) == 0:
            print('blue wins!!!!')
            return 'blue'
        chosen = game_in_func.loc[game_in_func['label'] == 'chosen', 'word'].tolist()
        if len(chosen) > 0:
            for word in chosen:
                game_in_func_dictionary[word] = 3
                # lab = game_in_func_dictionary[word]
                # del game_in_func_dictionary[word]
                # game_in_func_dictionary[' '] = lab
        game_in_func = game_in_func.loc[game_in_func['label'] != 'chosen', :]
        game_in_func.to_csv('game_in_func.csv')
        if start == 'blue':
            start = 'red'
        else:
            start = 'blue'
print(play_game(game))
