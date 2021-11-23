from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import re

genres = ['nhac-tre', 'tru-tinh',
          'rap-viet', 'tien-chien', 'rock-viet', 'cach-mang', 'thieu-nhi']


def lyric_preprocess(lyric):
    if lyric != None:

        lyric = re.sub(
            r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', '', str(lyric))

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

        lines = []

        for line in lyric.lower().strip().split('\n'):
            if line != '' and not line.startswith('đk') and not line.startswith('dk') and not line.startswith('[') and not line.__contains__(':') and len(line) > 5 and line.strip() != title.lower().strip():
                line = re.sub(
                    r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', ' ', str(line))
                line = re.sub(r'\s+', ' ', str(line))
                lines.append(line.strip())

        lyric = ' '.join(lines).strip()

        print(lyric)

        if lyric.find('hiện chưa có lời bài hát nào') != -1:
            lyric = None

    except:

        pass

    return [title, url, lyric]
