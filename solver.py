import numpy as np
import csv

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
def charCounter(words):
    char_counts = np.zeros(26, dtype= int)

    #iterate through the entire file to count the occurences of all letters
    for i in range(len(words)):
        for j in range(5):
            char_counts[ord(words[i][j])-97] += 1

    #display the character counts
    print(char_counts)

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

#solves the game of wordle
def solver(exceldata):
    sorted = np.sort(exceldata, order=["scores"], kind="mergesort")[::-1]
    

def main():
    txt_file_name = Path('files/Library.txt')
    csv_file_name = Path("files/word_scores.csv")

    #generates the excel sheet with scores if the file does not exist
    if(csv_file_name.is_file() == False):
        words = txtFileReader(txt_file_name)
        char_score = charCounter(words)
        generateExcel(words, char_score, csv_file_name)
    else:
        print("[FILE HAS ALREADY BEEN GENERATED, NOW TRYING TO SOLVE]")

    exceldata = excelFileReader(csv_file_name)
    solver(exceldata)

main()