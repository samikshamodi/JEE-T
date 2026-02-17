import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

df = pd.read_csv('IRdata2.csv')

df.head()

df.drop(['question', 'imageURL', 'options', 'answer', 'explaination'], inplace=True, axis=1)
df.head()

correct = np.random.randint(2, size=len(df))
times = np.random.uniform(low=1, high=103, size=len(df))

df['correct'] = correct
df['time_taken'] = times

df.head()



"""## Difficulty code"""

df.describe()



# time score: ln(1+x)
# accuracy score: 0.75x for correct, 1.5x for incorrect, repeated wrong answers for same question will increase the multiplier

diff = np.zeros(len(df))

for i in range(len(df)):
  time = df['time_taken'][i]
  acc = df['correct'][i]
  score = np.log(1 + time)
  if(acc == 1):
    score *= 0.75
  else:
    score *= 1.5
  
  diff[i] = score

df['difficulty'] = diff

df.describe()



df[df['correct'] == 1].describe()

df[df['correct'] == 0].describe()



domaindf = df.groupby('domain').mean()
domaindf

domaindf.describe()['difficulty']['25%']

# classification
# below 25% = easy, 25-75 = intermediate, above 75% = hard

tier = []
for val in domaindf['difficulty']:
  if(val < 4.1188):
    tier.append('easy')
  elif(val < 4.3135):
    tier.append('intermediate')
  else:
    tier.append('hard')

domaindf['tier'] = tier

domaindf

domaindf['tier'].value_counts()