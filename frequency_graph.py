import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

def charCounter(words):
    char_counts = np.zeros(26, dtype= int)

    #iterate through the entire file to count the occurences of all letters
    for i in range(len(words)):
        for j in range(5):
            char_counts[ord(words[i][j])-97] += 1

    return char_counts

#file paths
library_file_name = Path("files/Library.txt")
guesses_file_name = Path("files/Guesses.txt")
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

plt.subplot(1, 2, 1)
words = np.loadtxt(library_file_name, dtype= str)
out = charCounter(words)
df = pd.DataFrame({"Alphabet":alphabet, "Counts":out})
df = df.sort_values(by="Counts",ascending= False)
plt.bar(df["Alphabet"],df["Counts"],color ='lightseagreen',width = 0.75)
plt.xlabel("Valid Guesses Character Count")

plt.subplot(1, 2, 2)
words = np.loadtxt(guesses_file_name, dtype= str)
out = charCounter(words)
df = pd.DataFrame({"Alphabet":alphabet, "Counts":out})
df = df.sort_values(by="Counts",ascending= False)
plt.bar(df["Alphabet"],df["Counts"],color ='lightseagreen',width = 0.75)
plt.xlabel("Hidden Words Character Count")


plt.show()

