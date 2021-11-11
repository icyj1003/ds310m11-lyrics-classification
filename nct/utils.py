from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import re

genres = ['nhac-tre', 'tru-tinh',
          'rap-viet', 'tien-chien', 'rock-viet', 'cach-mang', 'thieu-nhi']


def lyric_preprocess(lyric):
    if lyric != None:
        # xóa các ký tự không cần thiết
        lyric = re.sub(
            r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', '', str(lyric))
        # xóa khoảng trắng thừa
        lyric = re.sub(r'\s+', ' ', str(lyric))
        return lyric
    else:
        return None


def getUrls(genre='nhac-tre'):

    if genre not in genres:

        raise ValueError(f"Nhập vào một trong các thể loại sau: {genres}")

    else:

        url_prefix = f'https://www.nhaccuatui.com/bai-hat/{genre}-moi.'

        url_suffix = '.html'

        pnum = 25

        songs = []

        with tqdm(total=25, desc=f"Đang lấy url {genre}") as pbar:

            for i in range(1, pnum + 1):

                url = url_prefix + str(i) + url_suffix

                page = requests.get(url)

                soup = BeautifulSoup(page.content, 'html.parser')

                songs = songs + soup.find_all('div', class_='info_song')

                pbar.update(1)

        pbar.close()

        print('Hoàn tất')

        return [song.find('a').get('href') for song in songs]


def getInfo(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = None

    artis = None

    lyric = None

    try:
        lyric = soup.find('p', class_='pd_lyric trans').text

        title_artis = soup.find('div', class_='name_title').text.split('-')

        title = title_artis[0].strip()

        artis = title_artis[1].strip()

        lyric = [line.strip() for line in lyric.lower().strip().split('\n')
                 if line.find(':') == -1 and line != title.lower() and line != '']

        lyric = ' '.join(lyric).strip()

        lyric = lyric_preprocess(lyric)

    except:

        pass

    return [title, artis, lyric]


def getLyrics(songs, genre):

    lyrics = []

    with tqdm(total=len(songs), desc=f'Đang lấy lyric {genre}') as pbar:

        for song in songs:

            songInfo = getInfo(song)

            songInfo.append(genre)

            lyrics.append(songInfo)

            pbar.update(1)

    return lyrics
