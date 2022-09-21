import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import utils

matplotlib.use("TkAgg")
pairings = [utils.random_within_circle() for _ in range(100000)]

# plt.plot(pairings, 'o')

plt.plot([pairings[x][0] for x in range(len(pairings))], [pairings[y][1] for y in range(len(pairings))], 'o')
plt.show()