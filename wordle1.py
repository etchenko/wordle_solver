import sys
import click
from threading import Thread
import time
import random
import math

@click.command()
@click.option('--ans', help = 'The answer to the wordle')
@click.option('--test', is_flag = True, default = False, help ='Run a test on all of the words')
@click.option('--play', is_flag = True, default = False, help = 'Marker to play wordle with a random word')

#
# A program to solve wordle puzzles, or to play wordle games
#
def main(ans, test, play):
    print("Welcome to Wordle Solver.")
    # Read the word list
    with open('words.txt','r') as input:
        inputs = input.readlines()
        words = []
        for word in inputs:
            words.append(word[:-1])
        
        # If answer is given run automatically
        if play:
            wordle_play()
        elif ans:
            print("The program will run automatically, showing you the guesses and the output to the guesses.")
            print("A '_' signifies that the letter is not present in the answer\nA '.' signifies that it does but is in the wrong spot\nA 'x' signifies that the letter was correct.")
            guesser(words, False, ans, test)
        # Run the simulation on all of the wordle words
        elif test:
            with open('previous_words.txt','r') as previous:
                inputs = previous.readlines()
                sample = []
                for word in inputs:
                    sample.append(word[:-1].lower())
                start_time = time.time()
                sum1, sum2, sum3 = 0, 0, 0
                print("Starting...")
                for i, word in enumerate(sample): 
                    sum1 += guesser(words, False, word, test)
                    sum2 += guesser2(words, False, word, test)
                    sum3 += guesser3(words, False, word, test)
                    if i % 100 == 0:
                        print(i)
                av1 = sum1 / len(sample)
                av2 = sum2 / len(sample)
                av3 = sum3 / len(sample)
                print(av1, av2, av3)
                print("--- %s seconds ---" % (time.time() - start_time))
        # Manually input results
        else:
            print("The program will print it's guess, and you must input the reply from the wordle game")
            print("A '_' signifies that the letter is not present in the answer\nA '.' signifies that it does but is in the wrong spot\nA 'x' signifies that the letter was correct.")
            guesser(words, True, ans, test)

#
# The original gusser, which works solely using frequencies of the letters
#
def guess(words):
    dict1 = {}
    for word in words:
        for letter in word:
            if letter in dict1.keys():
                dict1[letter] = dict1[letter] + 1
            else:
                dict1[letter] = 1
    dict1 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1])}
    best, best_word = 0,''
    dict2 = {}
    for word in words:
        letters = list(set(word))
        sums = sum([dict1[key] for key in letters])
        dict2[word] = sums
        if sums > best:
            best = sums
            best_word = word
    dict2 = {k: v for k, v in sorted(dict2.items(), key=lambda item: item[1], reverse = True)}
    dict3 = dict(list(dict2.items())[:10])
    return best_word

def guess_freq(words):
    # Populate the frequency lists
    dict_array = [dict() for x in range(6)]
    for word in words:
        for i, letter in enumerate(word):
            if letter in dict_array[i].keys():
                dict_array[i][letter] = dict_array[i][letter] + 1
            else:
                dict_array[i][letter] = 1
    for dict1 in dict_array:
        dict1 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1])}
    best, best_word = 0,''
    word_rankings = {}
    for word in words:
        sum = 0
        for i, letter in enumerate(word):
            sum += dict_array[i][letter]
        if sum > best:
            best = sum
            best_word = word
    # word_rankings = {k: v for k, v in sorted(word_rankings.items(), ley = lambda item: item[1], reverse = True)}
    return best_word

def guess_info_loc(words):
    dict_array = [dict() for x in range(6)]
    for word in words:
        for i, letter in enumerate(word):
            if letter in dict_array[i].keys():
                dict_array[i][letter] = dict_array[i][letter] + 1
            else:
                dict_array[i][letter] = 1
    for dict1 in dict_array:
        dict1 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1])}
    best, best_word = -10000,'i'
    word_rankings = {}
    for i, word in enumerate(words):
        sum = 0
        for j, letter in enumerate(word):
            prob = dict_array[j][letter]/len(words)
            sum += -prob*math.log(prob,2)
        if sum > best:
            best = sum
            best_word = word
    # word_rankings = {k: v for k, v in sorted(word_rankings.items(), ley = lambda item: item[1], reverse = True)}
    return best_word

def guess_info(words):
    best, best_word = len(words),''
    for word in words:
        for ans in words:



    

#
# The main function of the program which contains the functionality for guessing a wordle word
# Currently using: Frequency guesser
#
def guesser(words, manual, answer, test):
    guesses = 0
    reply = ''
    finish = False
    while not finish:
        if len(words) < 1:
            print("Word not found")
            quit()
        word = guess(words)
        guesses += 1
        if manual:
            print("The guess is: " + word)
            reply = input("Output of guess:")
        else:
            reply = ''
            for i, letter in enumerate(word):
                if not (letter in answer):
                    reply += '-'
                elif letter != answer[i]:
                    reply += '.'
                else:
                    reply += 'x'
            if not test:
                print(word)
                print(reply)
        if reply == 'xxxxx':
            finish = True
        words = limit_words(words, reply, word)
    if manual or not test:
        print("The answer was: " + words[0])
        print(f"It was guessed in {guesses} guesses")
    return guesses

def guesser2(words, manual, answer, test):
    guesses = 0
    reply = ''
    finish = False
    while not finish:
        if len(words) < 1:
            print("Word not found")
            quit()
        word = guess_info_loc(words)
        guesses += 1
        if manual:
            print("The guess is: " + word)
            reply = input("Output of guess:")
        else:
            reply = ''
            for i, letter in enumerate(word):
                if not (letter in answer):
                    reply += '-'
                elif letter != answer[i]:
                    reply += '.'
                else:
                    reply += 'x'
            if not test:
                print(word)
                print(reply)
        if reply == 'xxxxx':
            finish = True
        words = limit_words(words, reply, word)
    if manual or not test:
        print("The answer was: " + words[0])
        print(f"It was guessed in {guesses} guesses")
    return guesses

def guesser3(words, manual, answer, test):
    guesses = 0
    reply = ''
    finish = False
    while not finish:
        if len(words) < 1:
            print("Word not found")
            quit()
        if guesses < 1:
            word = guess_info_loc(words)
        else:
            word = guess(words)
        guesses += 1
        if manual:
            print("The guess is: " + word)
            reply = input("Output of guess:")
        else:
            reply = ''
            for i, letter in enumerate(word):
                if not (letter in answer):
                    reply += '-'
                elif letter != answer[i]:
                    reply += '.'
                else:
                    reply += 'x'
            if not test:
                print(word)
                print(reply)
        if reply == 'xxxxx':
            finish = True
        words = limit_words(words, reply, word)
    if manual or not test:
        print("The answer was: " + words[0])
        print(f"It was guessed in {guesses} guesses")
    return guesses
#
# Limits the number of possible answers for the wordle puzzle based on the reply for the guess
#
def limit_words(words, reply, guess):
    output = []
    for word in words:
        present = True
        for i, type in enumerate(reply):
            if type == 'x':
                if word[i] != guess[i]:
                    present = False
            elif type == '.':
                if word[i] == guess[i] or not (guess[i] in word):
                    present = False
            else:
                if guess[i] in word:
                    present = False
        if present:
            output.append(word)
    return output

#
# G
#
def get_reply(word, ans):


#
# Play a wordle game using random words from the dictionary
#
def wordle_play():
    print("Not finished yet")

if __name__ == '__main__':
    main()