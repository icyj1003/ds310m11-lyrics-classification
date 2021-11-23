import os
import pandas as pd

parts = []
dir = os.listdir(path='./data')

for file in dir:
    parts.append(file.replace('.csv', ''))

header = ['title', 'singer', 'lyric', 'genre']
df = pd.DataFrame()
count = 0
for file in dir:
    print(file)
    if file != 'nct.csv':
        part = pd.read_csv(f'./data/{file}')
        part.drop_duplicates(subset=['lyric'], inplace=True)
        df = pd.concat([df, part], ignore_index=True)
        count = count + 1
        print(f"Đã hợp nhất {count} files!")
print(df.shape)
df.to_csv('./data/nct.csv', index=False, encoding='utf-8-sig')
