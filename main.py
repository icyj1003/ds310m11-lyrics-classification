from nct.utils import getInfo, getUrls, getLyrics
from nct.repos import nctGenres
import pandas as pd
from tqdm import tqdm

lyrics = []

for genre in nctGenres():

    songs = getUrls(genre=genre)

    temp = getLyrics(songs=songs, genre=genre)

    lyrics = lyrics + temp

    dfG = pd.DataFrame(temp, columns=['title', 'singer', 'lyric', 'genre'])

    dfG.to_csv(f'./data/{genre}.csv', index=False, encoding='utf-8-sig')

df = pd.DataFrame(lyrics, columns=['title', 'singer', 'lyric', 'genre'])

df.to_csv('./data/nct.csv', index=False, encoding='utf-8-sig')
