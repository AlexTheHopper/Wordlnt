import random
import requests
import string
from numpy.random import choice
from english_words import get_english_words_set

###Welcome to Wordln't!###
###This game will ask for the user to enter a word length and number of guesses###
###It will then run a Wordle type game with the input settings###
#Retrieves list of potential words to use
def getWords(wordLength):

    list = []
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    wordslist1 = response.content.splitlines()

    for x in wordslist1:
        if len(x) == wordLength:
            list.append(x.decode('utf-8'))

    return(list)

#Retrieves a different list of potential words to use
def getwords2(wordLength):

    allwords = get_english_words_set(['web2'], lower=True)
    lengthwords = [x for x in allwords if len(x)==wordLength]
    return(lengthwords)

#Plays one game of Wordln't
def playgame(answer, numGuesses, wordLength, wordsList):

    #Prepares variables for game
    #Tracking how many guesses have been had
    guessCount = 0
    #List for outputting previous guesses and feedback
    feedbackGrid = []
    #List of correct letters in the answer word for creating feedback
    answerLetters = [x for x in answer]

    #Symbols for feedback, akin to green, orange and grey in Wordle
    correct = "+"
    semicorreect = "."
    wrong = " "

    print("Hello you! Welcome to Wordln't!")
    print("You are playing with word length:",wordLength,"and you have", numGuesses,"guesses.")
    print("Letters in the correct space will show as",correct)
    print("Correct letters in the incorrect space will show as",semicorreect)
    

    while guessCount < numGuesses:

        #Ensures that the guess could potentially be correct
        while True:
            guess = input("Enter guess:").lower()
            if guess in wordsList:
                break
            else:
                print("Word not in list.")

        #Adds guess to output list
        feedbackGrid.append(guess.upper())
        #Creates variables for guess analysis
        guessLetters = [x for x in guess]
        dummyAnswerLetters = answerLetters[:]
        feedbackTemp = [wrong]*wordLength

        #dummyAnswerLetters required for double letter problems

        
        #check which letters are there and in correct spot
        for i in range(len(guessLetters)): 
            if guessLetters[i] == answerLetters[i]:
                feedbackTemp[i] = correct
                dummyAnswerLetters[dummyAnswerLetters.index(guessLetters[i])] = ' '        

        #check which letters are there but in wrong spot
        for i in range(len(guessLetters)):
                if guessLetters[i] in dummyAnswerLetters and feedbackTemp[i] == wrong:
                    feedbackTemp[i] = semicorreect
                    dummyAnswerLetters[dummyAnswerLetters.index(guessLetters[i])] = ' '

            
        #Creates and appends guess feedback
        feedbackTemp = "".join(feedbackTemp)
        feedbackGrid.append(feedbackTemp)

        #Prints feedback to user
        print("==========")
        for i in feedbackGrid:
            print(i)
      
        #Cannot have more guesses than the limit
        guessCount += 1

        #Win condition
        if guess == answer:
            input("CONGRATS CHIEF YOU DID IT!! Press enter to play again")
            #Exits game and asks to replay
            return
        
    #Lose condition
    print("You lose! Try again!")
    print("The word was", answer)


while True:

    #User input for word length and number of guesses
    #Will keep asking until numbers are entered
    wordLength = ""
    numGuesses = ""
    while not isinstance(wordLength, int) and not isinstance(numGuesses, int):
        wordLength = input("Enter length of word you want to guess:")
        numGuesses = input("Enter how many guesses you want to have:")
        try:
            wordLength = int(wordLength)
            numGuesses = int(numGuesses)
        except:
            print('Please enter numbers...')

    #Retrieve word list
    wordsList = getwords2(wordLength)
    #Choose random word from list
    randomWord = random.choice(wordsList)
    #Play game with chosen settings
    playgame(randomWord, numGuesses, wordLength, wordsList)


