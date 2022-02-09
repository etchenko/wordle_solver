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
# A program to play and solve Wordle puzzles
# Using the input options, you can either input the answer word to the program
# in which case it will play wordle until it guesses the word and output the number of guesses.
# You can also have it continuosly feed you guesses while you feed back replies, 
# And finally it can run a test of a given algorithm against all the possible 5 letter words to see
# how well the algorithm can guess
#
def main(ans, test, play):
    print("Welcome to Wordle Solver.")
    # Read the word list from the file
    with open('words.txt','r') as input:
        inputs = input.readlines()
        words = []
        for word in inputs:
            words.append(word[:-1])
        
        # Play the game with randomly generated words
        if play:
            wordle_play()
        # An answer was provided, run the program automatically
        elif ans:
            print("The program will run automatically, showing you the guesses and the output to the guesses.")
            print("A '_' signifies that the letter is not present in the answer\nA '.' signifies that it does but is in the wrong spot\nA 'x' signifies that the letter was correct.")
            guesser(words, False, ans, test, guess)
        # Run the simulation on all of the wordle words to test guessing ability
        elif test:
            # Get all previous wordle answers
            with open('previous_words.txt','r') as previous:
                inputs = previous.readlines()
                sample = []
                for word in inputs:
                    sample.append(word[:-1].lower())
                # Time the runtime
                start_time = time.time()
                # Run the three different guessing strategies against each other
                sum1, sum2, sum3 = 0, 0, 0
                print("Starting...")
                # Run the wordle guesser for each word in the dictionary
                for i, word in enumerate(sample): 
                    sum1 += guesser(words, False, word, test, guess)
                    sum2 += guesser(words, False, word, test, guess_freq)
                    if i % 100 == 0:
                        print(i)
                # Find the averages of the guesses
                av1 = sum1 / len(sample)
                av2 = sum2 / len(sample)
                # Print the averages of the guesses
                print(av1, av2)
                print("--- %s seconds ---" % (time.time() - start_time))
        # Manually input results
        else:
            print("The program will print it's guess, and you must input the reply from the wordle game")
            print("A '_' signifies that the letter is not present in the answer\nA '.' signifies that it does but is in the wrong spot\nA 'x' signifies that the letter was correct.")
            # Run the main guesser
            guesser(words, True, ans, test)

#
# A guesser which looks at the frequency of each letter in all of the words,
# and attempts to maximize the amount of high probability unique letters in the guess
#
def guess(words):
    dict1 = {}
    # Cycle through the dictionary and add upp the frequencies of each letter
    for word in words:
        for letter in word:
            # Add the letter to the frequency dict
            if letter in dict1.keys():
                dict1[letter] = dict1[letter] + 1
            else:
                dict1[letter] = 1
    best, best_word = 0,''
    # Find the word which mazimizes the unique probabilties
    for word in words:
        # Extract all the unique letters in the word
        letters = list(set(word))
        # Sum up the frequencies
        sums = sum([dict1[key] for key in letters])
        # Check if it is the best
        if sums > best:
            best = sums
            best_word = word
    
    return best_word

#
# A guesser which makes a word guess based on the frequencies of letters
# in each letter index in the word
#
def guess_freq(words):
    # Populate the frequency lists for each location
    dict_array = [dict() for x in range(6)]
    for word in words:
        for i, letter in enumerate(word):
            if letter in dict_array[i].keys():
                dict_array[i][letter] = dict_array[i][letter] + 1
            else:
                dict_array[i][letter] = 1
    # Find the best word
    best, best_word = 0,''
    word_rankings = {}
    for word in words:
        sum = 0
        for i, letter in enumerate(word):
            sum += dict_array[i][letter]
        if sum > best:
            best = sum
            best_word = word
    return best_word

#
# A guesser which makes a guess based on a scoring system for how 
# much information it gives about each of the possible answers that are left
#
def guess_info(words):
    # Find the score of each of the words
    best, best_word = 0,''
    for word in words:
        lengths = []
        for ans in words:
            reply = get_reply(word, ans)
            score = 0
            for i in reply:
                if i == '.':
                    score += 3
                elif i == 'x':
                    score += 5
                else:
                    score += 2
            lengths.append(score)
        av = sum(lengths)/len(lengths)
        if av > best:
            best = av
            best_word = word
    return best_word


#
# The main function of the program which contains the functionality for guessing a wordle word
# The specific guessing algorithm is passed into the function as an argument
#
def guesser(words, manual, answer, test, guess_func):
    guesses, reply, finish = 0, '', False
    # Continue guessing until the word is guessed
    while not finish:
        # This means there are no words left that match
        if len(words) < 1:
            print("Word not found")
            quit()
        # Find the guess
        word = guess_func(words)
        guesses += 1
        # Ask for reply from user
        if manual:
            print("The guess is: " + word)
            reply = input("Output of guess:")
        else:
            # Calculate the reply string
            reply = get_reply(word, answer)
            if not test:
                print(word)
                print(reply)
        # The word was guessed!
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
# Compute the reply string based on the guess and answer
#
def get_reply(word, answer):
    reply = ''
    for i, letter in enumerate(word):
        if not (letter in answer):
            reply += '-'
        elif letter != answer[i]:
            reply += '.'
        else:
            reply += 'x'
    return reply

#
# Play a wordle game using random words from the dictionary
#
def wordle_play():
    print("Not finished yet")

if __name__ == '__main__':
    main()