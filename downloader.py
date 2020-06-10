import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os


def find_links():
    """
    Returns the links that contain the xls files
    """

    url = 'https://www.statistics.gr/el/statistics/-/publication/STO04/'

    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html5lib')

    history_wrapper = soup.find('div', {'class': 'history-wrapper'})

    links = []

    for a in history_wrapper.find_all('a'):
        name = a.find('div').text
        if re.search('^4.*201[1-5]$', name):
            link = urljoin(url, a['href'])
            links.append((name[-4:], link))  # keep only the year

    return links


def download_files(links, save_dir = 'xls_files/'):
    """
    Downloads the desirable xls files
    """

    for name, url in links:
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, 'html5lib')

        a = soup.find('a', string=re.compile(r'Αφίξεις μη κατοίκων από το εξωτερικό'
                                              ' ανά χώρα προέλευσης και μέσο μεταφοράς'))

        resp = requests.get(a['href'])

        os.makedirs(os.path.dirname(save_dir), exist_ok=True)
        output = open(os.path.join(save_dir, name + '.xls'), 'wb')
        output.write(resp.content)
        output.close()
        
        print('Year {} dataset was successfully downloaded!'.format(name))


if __name__ == '__main__':

    links = find_links()
    download_files(links)
