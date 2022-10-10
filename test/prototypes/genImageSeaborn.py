import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import statistics

height = 24
width = 32
pixel_columns = [f'pixel_{i}' for i in range(width * height)]
df = pd.read_csv("readcsv.csv")

row = df.iloc[0] # grab next row
pixels = np.array(row).reshape(height, width)
min,max = np.min(df.values), np.max(df.values)
std_deviation = statistics.pstdev(row)
mean = sum(row) / len(row)
print(f"The mean reading is {mean} and standard deviation is {std_deviation}")
ax = sns.heatmap(pixels, vmin = (mean-(2*std_deviation)), vmax =(mean+(2*std_deviation)), center = 0, linewidth=0.5) #Applying range rule of thumb from stat200
plt.show()