import numpy as np

def fileReader():
    words = np.loadtxt("Library.txt", dtype= str)
    char_counts = np.zeros(26, dtype= int)

    #display the total number of words for debugging
    print(len(words))

    for i in range(len(words)):
        for j in range(5):
            

    return words

#def charcounter(words):


def main():
    words = fileReader()
    #charcounter(words)

main()