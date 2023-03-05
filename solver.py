import numpy as np

def fileReader():
    words = np.loadtxt("Library.txt", dtype= str)
    char_counts = np.zeros(26, dtype= int)

    #display the total number of words
    print(len(words))

    #iterate through the entire file to count the occurences of all letters
    for i in range(len(words)):
        for j in range(5):
            char_counts[ord(words[i][j])-97] += 1

    #display the character counts
    print(char_counts)

    return words

#def charcounter(words):


def main():
    words = fileReader()
    #charcounter(words)

main()