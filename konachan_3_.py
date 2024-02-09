from os import chdir, mkdir, listdir, getcwd, rename
from os.path import exists
from wget import download
from shutil import rmtree
from requests import get
from bs4 import BeautifulSoup


URL_SCHEMA = 'http'


class KonaChan:
    def __init__(self):
        self._url = 'http://konachan.net/artist?page='
        self._last_page = None
        self._dir_name = 'wallpapers'
        self._last_last = []
        self._page_num = None
        self._oren = []
        self._ques = None
        self._true_artist = []

    def _last_item(self):
        r = get(self._url + str(1)).text
        soup = BeautifulSoup(r, 'lxml')
        for j in soup.find_all('a'):
            con = j.get('href')
            if con.startswith('/artist?page='):
                self._last_last.append(con)
        for i in self._last_last:
            to_int = i.replace('/artist?page=', '')
            self._oren.append(int(to_int))
        self._last_page = max(self._oren)
        print('\n                         >>> all page == {} <<<'.format(max(self._oren)))

    def artist_urls(self, url):
        oki = 'http://konachan.net' + url
        print('        {}'.format(oki))
        r = get(oki).text
        soup = BeautifulSoup(r, 'lxml')
        for j in soup.find_all('a', class_='directlink smallimg'):
            con = j.get('href')
            if not con.startswith(URL_SCHEMA):
                con = f"{URL_SCHEMA}:{con}"
            download(con)

    def get_true_artist(self):
        self._last_item()
        gg = self._last_page
        print("""
        1) Download wallpapers [ arts, pics ] starts from 1st page it will
                try download already downloaded wallpapers and [ arts, pics ] will be
                        with doublicates, but Rename kills doublicates
        2) You can start from some page
                if you already downloaded 3 pages
                        you can start from 4
        3) Rename wallpapers [ arts, pics ]
        4) And of course Clear dir wallpapers
        """)
        try:
            ques = eval(input('        Well, what do you want?:_ '))
            self._ques = ques
        except Exception:
            print('        Integer from 1 to 4')
        if self._ques == 1:
            if not exists(self._dir_name):
                mkdir(self._dir_name)
            chdir(self._dir_name)
            for a in range(1, gg + 1):
                print('\nGot:__ ', self._url + str(a))
                r = get(self._url + str(a)).text
                soup = BeautifulSoup(r, 'lxml')
                for i in soup.find_all('td'):
                    for j in i.find_all('a'):
                        con = j.get('href')
                        if con.startswith('/artist/show'):
                            self._true_artist.append(con)
                for k in self._true_artist:
                    self.artist_urls(k)
                self._true_artist.clear()

        elif self._ques == 2:
            if not exists(self._dir_name):
                mkdir(self._dir_name)
            chdir(self._dir_name)
            try:
                page_num = eval(input('        From what the page you wanna start?:_ '))
                self._page_num = page_num
            except Exception:
                print('      Integer number between your start and all page')
            for a in range(self._page_num, gg + 1):
                print('\nGot:__ ', self._url + str(a))
                r = get(self._url + str(a)).text
                soup = BeautifulSoup(r, 'lxml')
                for i in soup.find_all('td'):
                    for j in i.find_all('a'):
                        con = j.get('href')
                        if con.startswith('/artist/show'):
                            self._true_artist.append(con)
                for k in self._true_artist:
                    self.artist_urls(k)
                self._true_artist.clear()

        elif self._ques == 3:
            if exists(self._dir_name):
                chdir(self._dir_name)
                ben = listdir(getcwd())
                for i in ben:
                    try:
                        ken = i.split('%')[2]
                        rename(i, '{}'.format(ken))
                    except Exception:
                        pass
            else:
                print('        Can not find this dir: ', self._dir_name)

        elif self._ques == 4:
            if exists(self._dir_name):
                yes = input('        Are you sure to remove dir wallpapers? [Y/n]:_ ')
                if yes.upper() == 'Y':
                    rmtree(self._dir_name)
                else:
                    pass
            else:
                print('      I can not find dir ', self._dir_name)


if __name__ == '__main__':
    run = KonaChan()
    run.get_true_artist()
