import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

scores = Path("files/word_scores.csv")

df = pd.read_csv(scores, names=["word","score"])
df = df.sort_values(by="score",ascending= False)

print(df)