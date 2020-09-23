import pandas as pd
import os
import numpy as np
import os

frames = []
folder = 'to_combine/'
for file in os.listdir(folder):
    if os.path.splitext(file)[-1] == '.csv':
        frames.append(pd.read_csv(folder+os.path.splitext(file)[0]+'.csv'))

print(frames[2]['age'].unique())
print(frames[2]['rate'].unique())
print(frames[2]['votes'].unique())
print(frames[2]['genres'].unique())
print(frames[2]['studio'].unique())
print(frames[2]['year'].unique())
print(frames[2]['season'].unique())
print(frames[2]['watches'].unique())
