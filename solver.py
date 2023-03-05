import numpy as np
import csv

from pathlib import Path

#reads the text file and stores it into a variable
#returns the variable holding all the words
def fileReader():
    words = np.loadtxt(Path('files/Library.txt'), dtype= str)

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

        writer.writerow(["words","scores"])

        for i in range(len(words)):
            score = 0

            for j in range(5):
                score += char_score[ord(words[i][j])-97]

            writer.writerow([words[i],score])

            print(words[i] +" "+repr(score))

def main():
    file_name = Path("files/word_scores.csv")

    if(file_name.is_file() == False):
        words = fileReader()
        char_score = charCounter(words)
        generateExcel(words, char_score, file_name)
    else:
        print("[FILE HAS ALREADY BEEN GENERATED]")

main()