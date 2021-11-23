from nct.utils import getInfo, getUrls
from nct.repos import nctGenres
import pandas as pd
from tqdm import tqdm

count = 0

gList = nctGenres()

for item in gList:

    print(item, count)

    count = count + 1

genres = [gList[int(input('Genre: '))]]

for genre in genres:

    songs = getUrls(genre=genre)

    lyrics = []

    with tqdm(total=len(songs), desc=f'Đang lấy lyric {genre}') as pbar:

        for song in songs:

            songInfo = getInfo(song)

            if songInfo[2] != None:

                songInfo.append(genre)

                lyrics.append(songInfo)

            pbar.update(1)

    dfG = pd.DataFrame(
        lyrics, columns=['title', 'url', 'lyric', 'genre'])

    dfG.to_csv(f'./data/{genre}.csv', index=False, encoding='utf-8-sig')
