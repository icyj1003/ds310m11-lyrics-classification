import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from nct.utils import getInfo
from nct.repos import nctGenres

url = input('Playlist URL: ')

count = 0
gList = nctGenres()

for item in gList:

    print(item, count)

    count = count + 1

genre = gList[int(input('Genre: '))]

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('a', class_='name_song')

# df = pd.read_csv(f'./data/{genre}.csv')

with tqdm(total=len(results), desc='Đang lấy playlist') as pbar:

    for item in results:

        song = item.get('href')

        if song.find('playlist') != -1:

            pbar.close()

            break

        songInfo = getInfo(song)

        if songInfo[2] != None:

            songInfo.append(genre)

            songInfo = pd.Series(
                songInfo, index=['title', 'url', 'lyric', 'genre'])

            df = df.append(songInfo, ignore_index=True)

        pbar.update(1)

# df.to_csv(f'./data/{gList[genre]}.csv', index=False, encoding='utf-8-sig')
