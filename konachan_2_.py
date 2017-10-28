from requests import get
from bs4 import BeautifulSoup


class KonaChan:
    def __init__(self):
        self._url = 'http://konachan.net/artist?page='
        self._last_page = None
        self._file = ""
        self._last_last = []
        self._activate_name = []
        self._artist_name = ""
        self._oren = []
        self._get_second = []
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

    def artist_name(self, url):
        r = get(url).text
        soup = BeautifulSoup(r, 'lxml')
        for i in soup.find_all('h2'):
            con = i.text
            if len(con) > 0:
                self._artist_name = con.strip()
                print(con.strip())

    def artist_urls(self, url):
        oki = 'http://konachan.net' + url
        self.artist_name(oki)
        r = get(oki).text
        soup = BeautifulSoup(r, 'lxml')
        for i in soup.find_all('td'):
            for j in i.find_all('a'):
                con = j.get('href')
                if self._file in con:
                    self._activate_name.append(con)
        if len(self._activate_name) > 0:
            with open(self._file + '.txt', 'a') as file:
                file.write("\n\n{}".format(self._artist_name))
            for d in self._activate_name:
                with open(self._file + '.txt', 'a') as file:
                    file.write("\n      '{}',".format(d))
                print('     ', d)
        self._activate_name.clear()
        print('\n\n')

    def get_true_artist(self):
        self._last_item()
        gg = self._last_page
        print("""
        if you want only artists page in 'twitter', just write twitter...
                if 'facebook' page -> facebook, 'pixiv' -> pixiv...
        """)
        wants_url = input('        What the artists page you want?:_ ')
        self._file = wants_url
        for a in range(1, gg + 1):
            print('Got: ', self._url + str(a))
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


if __name__ == '__main__':
    run = KonaChan()
    run.get_true_artist()
