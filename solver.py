import numpy as np
import csv
import re

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

#solves the game of wordle using statistical analysis and regular expressions
def solver(exceldata):
    sorted = np.sort(exceldata, order=["scores"], kind="mergesort")[::-1]
    temp = []

    for i in range(len(sorted)):
        if (all(count < 2 for count in charCounter(sorted["words"][i], False))):
            temp.append((sorted["words"][i],sorted["scores"][i]))

    noRepeats = np.asarray(temp, dtype=np.dtype([("words",np.unicode_,8), ("scores",np.int_)]))
    
    grey = ""
    yellow = ["","","","","",""]
    green = ""
    guesses_output = []

    for x in range(6):
        temp = []

        grey, yellow, green, regex = regexGen(grey, yellow, green, x, guesses_output)
        r = re.compile(regex)
        
        for i in range(len(noRepeats)):
            if(r.match(noRepeats["words"][i])):
                temp.append((noRepeats["words"][i], noRepeats["scores"][i]))

        if(len(temp) == 0):
            for i in range(len(sorted)):
                if(r.match(sorted["words"][i])):
                    temp.append((sorted["words"][i], sorted["scores"][i]))

        guesses_output = np.asarray(temp, dtype=np.dtype([("words",np.unicode_,8), ("scores",np.int_)]))

        if(len(guesses_output) > 4):
            for i in range(5):
                print(guesses_output[i])
        else:
            for i in range(len(guesses_output)):
                print(guesses_output[i])

#generates the regular expression to filter through the wordle accepted words list
#returns the grey, yellow and greens letters followed by the regular expression
def regexGen(grey, yellow, green, guess_count, guess):
    if(guess_count == 0):
        regex = re.compile('^[\w][\w][\w][\w][\w]')
    else:
        print("\nInput the color codes in a single line [NO SPACES]\n\t0: Grey\n\t1: Yellow\n\t2: Green\n")
        codes = input()

        print("codes "+codes)

        regex = "^"

        for i in range(5):
            if(codes[i] == "0"):
                grey += str(guess[0][0][i])
            elif(codes[i] == "1" or (len(yellow[i+1]) !=0 and codes[i] != "2")):
                yellow[0] += str(guess[0][0][i])

                yellow[i+1] += str(guess[0][0][i])

            elif(codes[i] == "2"):
                green += str(guess[0][0][i])

        print(yellow)

        yellow[0] = ''.join(sorted(yellow[0]))
        yellow[0] = re.sub(r'([a-z])\1+', r'\1', yellow[0])

        if(len(grey) > 0):
            regex += "(?!.*[" + grey + "])"

        for i in range(len(yellow[0])):
            regex += "(?=.*" + yellow[0][i] + ")"

        for i in range(5):
            if (codes[i] == "0"):
                regex += "[\w]"
            elif (codes[i] == "1"):
                regex += "[^" + yellow[i+1] + "]"
            elif (codes[i] == "2"):
                regex += "[" + str(guess[0][0][i]) + "]"

                for j in range(6):
                    yellow[j] = yellow[j].replace(str(guess[0][0][i]),"")
        
        print(regex)

    return grey, yellow, green, regex

def main():
    txt_file_name = Path('files/Library.txt')
    csv_file_name = Path("files/word_scores.csv")

    #generates the excel sheet with scores if the file does not exist
    if(csv_file_name.is_file() == False):
        words = txtFileReader(txt_file_name)
        char_score = charCounter(words, True)
        generateExcel(words, char_score, csv_file_name)
    else:
        print("[FILE HAS ALREADY BEEN GENERATED, NOW TRYING TO SOLVE]")

    exceldata = excelFileReader(csv_file_name)
    solver(exceldata)

main()