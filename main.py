import numpy as np
import csv
import re
import screen_reader as sr
import bot
import time
import os
import sys

from datetime import datetime
from pathlib import Path

#reads the text file and stores it into a variable
#returns the variable holding all the words
def txtFileReader(file_name):
    words = np.loadtxt(file_name, dtype= str)

    #display the total number of words
    print(len(words))

    return words

#counts all occurences of the letters
#returns the counts of all characters
def charCounter(words, generateMode):
    char_counts = np.zeros(26, dtype= int)

    if(generateMode):
        #iterate through the entire file to count the occurences of all letters
        for i in range(len(words)):
            for j in range(5):
                char_counts[ord(words[i][j])-97] += 1

        #display the character counts
        print(char_counts)

    else:
        for i in range(5):
            char_counts[ord(words[i])-97] += 1

    return char_counts

#creates an excel sheet with all the words and their scores
def generateExcel(words, char_score, file_name):
    with open(file_name, 'w+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        for i in range(len(words)):
            score = 0

            for j in range(5):
                score += char_score[ord(words[i][j])-97]

            writer.writerow([words[i],score])

            #prints the word and its score 
            print(words[i] +" "+repr(score))

#reads the generated csv file and creates a dataframe with words and scores
#returns the data from the csv file
def excelFileReader(file_name):
    data = np.loadtxt(file_name, delimiter=",", dtype=np.dtype([("words",np.unicode_,8),("scores",np.int_)]))

    return data

#generates the dictiionary of words used by the wordle solver
#returns the whole dictionary and the dictionary with repeated chars removed
def genDicts():
    temp = []
    wholeDict = np.sort(exceldata, order=["scores"], kind="mergesort")[::-1]

    for i in range(len(wholeDict)):
        if (all(count < 2 for count in charCounter(wholeDict["words"][i], False))):
            temp.append((wholeDict["words"][i],wholeDict["scores"][i]))

    noRepeats = np.asarray(temp, dtype=np.dtype([("words",np.unicode_,8), ("scores",np.int_)]))

    return wholeDict, noRepeats

#solves the game of wordle using statistical analysis and regular expressions
def solver(exceldata):    
    grey = ["","","","","",""]
    yellow = ["","","","","",""]
    green = ""
    guesses_output = []
    repeats = False

    for x in range(6):
        temp = []

        if(mode == "maz"):
            time.sleep(0.1)
        elif(mode == "ny"):
            time.sleep(3)

        grey, yellow, green, regex = regexGen(grey, yellow, green, x, guesses_output)
        r = re.compile(regex)
        
        for i in range(len(noRepeats)):
            if(r.match(noRepeats["words"][i])):
                temp.append((noRepeats["words"][i], noRepeats["scores"][i]))

        if(len(temp) == 0 or repeats == True):
            repeats = True
            for i in range(len(wholeDict)):
                if(r.match(wholeDict["words"][i])):
                    temp.append((wholeDict["words"][i], wholeDict["scores"][i]))

        guesses_output = np.asarray(temp, dtype=np.dtype([("words",np.unicode_,8), ("scores",np.int_)]))

        bot.pressString(guesses_output[0][0])
        guesses_output = guesses_output[0][0]

    winLoseGame(5)

def getCode(guess_count):
    codes = ""

    for i in range(5):
        codes = codes + sr.getPixelCode(points[guess_count-1][i])

    return codes

#generates the regular expression to filter through the wordle accepted words list
#returns the grey, yellow and greens letters followed by the regular expression
def regexGen(grey, yellow, green, guess_count, guess):
    if(guess_count == 0):
        regex = re.compile('^[\w][\w][\w][\w][\w]')
    else:
        codes = getCode(guess_count)

        if (codes == "22222"):
            winLoseGame(guess_count)

        regex = "^"

        #putting all the tiles into their appropriate colours
        for i in range(5):
            if(codes[i] == "0"):
                grey[0] += str(guess[i])
                grey[i+1] += str(guess[i])

            elif(codes[i] == "1" or (len(yellow[i+1]) !=0 and codes[i] != "2")):
                yellow[0] += str(guess[i])
                yellow[i+1] += str(guess[i])

            elif(codes[i] == "2"):
                green += str(guess[i])

        #sorting all of the yellow tiles and removing duplicates within the yellow
        yellow[0] = ''.join(sorted(yellow[0]))
        yellow[0] = re.sub(r'([a-z])\1+', r'\1', yellow[0])

        #very specific edge case where if there are duplicate letters one valid one invalid
        if(len(grey[0]) > 0 and len(green) > 0):
            pattern = "[" + green + "]"
            grey[0] = re.sub(pattern, '', grey[0])
                                            
            regex += "(?!.*[" + grey[0] + "])"
        elif(len(grey[0]) > 0 and len(yellow[0]) > 0):
            pattern = "[" + yellow[0] + "]"
            grey[0] = re.sub(pattern, '', grey[0])
                                            
            regex += "(?!.*[" + grey[0] + "])"
        else:
            regex += "(?!.*[" + grey[0] + "])"


        #creation of the positive lookahead for the yellow tiles
        if(len(yellow[0])>0):
            for i in range(len(yellow[0])):
                regex += "(?=.*"+ yellow[0][i] +".*)"


        for i in range(5):
            if (codes[i] == "0"):
                if(len(grey[i+1])>0):
                    regex += "[^" + yellow[i+1] + grey[i+1] + "]"
                else:
                    regex += "[\w]"
            elif (codes[i] == "1"):
                regex += "[^" + yellow[i+1] + grey[i+1] + "]"
            elif (codes[i] == "2"):
                regex += "[" + str(guess[i]) + "]"

                #if it's yellow prior, remove it from yellow if it is now green
                for j in range(6):
                    yellow[j] = yellow[j].replace(str(guess[i]),"")

    print(regex)

    return grey, yellow, green, regex

#game end condition
def winLoseGame(guess_count):
    
    if(play_again == True and mode == "maz"):
        global total_guess_count
        if(getCode(guess_count) != "22222"):
            global lose 
            lose +=1

            total_guess_count += 7
        else:
            global win
            win +=1

            total_guess_count += (guess_count + 1)

        os.system("cls")

        print("WIN: " + repr(win) + "\tLOSE: " + repr(lose) + "\t WINRATE: " + repr(float(win/(win+lose) * 100)) + "\tAVERAGE NO. GUESSES: " +repr(float(total_guess_count/(win+lose))))\

        if(win+lose == number_of_games):
            end_time =datetime.now()
            print("Total Time: {}".format(end_time-start_time))
            exit(0)
        else:
            bot.restart()
            solver(exceldata)

    elif(mode == "ny"):
        end_time =datetime.now()
        print("Total Time: {}".format(end_time-start_time))
        exit(0)
    else:
        end_time =datetime.now()
        print("Total Time: {}".format(end_time-start_time))
        exit(0) 


#defining the global variables
#change these variables if you want to test it out
make_image = False

#modes can either be "maz" or "ny"
mode = "ny"
play_again = False
number_of_games = 100

#setting up evaluation metrics
lose = 0
win = 0
total_guess_count = 0


sys.setrecursionlimit(5000)

#file paths
txt_file_name = Path('files/Library.txt')
csv_file_name = Path("files/word_scores.csv")

#detecting if the csv file exists, else generate a new one
if(csv_file_name.is_file() == False):
    words = txtFileReader(txt_file_name)
    char_score = charCounter(words, True)
    generateExcel(words, char_score, csv_file_name)

#loading the excel data
exceldata = excelFileReader(csv_file_name)

#generating agents vocabulary
wholeDict, noRepeats = genDicts()

#detecting the bounding boxes of the wordle game
points = sr.findPoints(make_image, mode)
click_point = points[0][0]
bot.focus(click_point)

if(mode == "maz"):
    bot.restart()

#runs the solving loop
start_time = datetime.now()
solver(exceldata)

