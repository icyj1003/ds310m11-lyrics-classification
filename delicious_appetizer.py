import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from nct.repos import nctGenres
import pandas as pd


def pick(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def gather(url):

    playlist = []

    try:

        playlist_page = pick(url)

        songs = playlist_page.find_all('h3', class_='name over-text')

        for song in songs:

            playlist.append(song.find('a').get('href'))

    except:

        pass

    return playlist


def peel(url, genre):

    lyric = None

    title = None

    artis = None

    try:

        song = pick(url)

        lyric = song.find(
            'div', class_='content_lyrics dsc-body').text.strip().rstrip('Xem hết')

        title = song.find('h1', class_='name_detail').text.strip()

        lines = []

        for line in lyric.lower().strip().split('\n'):
            if line != '' and not line.startswith('đk') and not line.startswith('dk') and not line.startswith('[') and not line.__contains__(':') and len(line) > 5 and line.strip() != title.lower().strip():
                line = re.sub(
                    r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', ' ', str(line))
                line = re.sub(r'\s+', ' ', str(line))
                lines.append(line.strip())

        lyric = ' '.join(lines).strip()

        if len(lines) < 3:
            lyric = None

    except:

        pass

    return (title, url, lyric, genre)


def collect():

    url = input('URL: ')

    num = int(input('Pages: '))

    count = 0

    gList = nctGenres()

    for item in gList:

        print(item, count)

        count = count + 1

    genre = gList[int(input('Genre: '))]

    lyrics = []

    with tqdm(total=num) as pbar:

        for i in range(1, num + 1):

            songs = gather(url + f'?p={i}')

            for song in songs:

                result = peel(song, genre)

                if result[2] != None:

                    lyrics.append(result)

            df = pd.DataFrame(
                lyrics, columns=['title', 'url', 'lyric', 'genre'])

            df.drop_duplicates()

            df.to_csv(f'./nhacvn/{genre}.csv',
                      index=False, encoding='utf-8-sig')

            pbar.update(1)

    df = pd.DataFrame(
        lyrics, columns=['title', 'url', 'lyric', 'genre'])

    df.drop_duplicates()

    df.to_csv(f'./nhacvn/{genre}.csv', index=False, encoding='utf-8-sig')


collect()
