import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import os

url = input('Enter issuu URL: ')
save_path = input('Enter path to save images to: ')
r = requests.get(url.strip())  # download url
soup = BeautifulSoup(r.content, 'html.parser')  # extract HTML elements from the url

title = soup.find('meta', attrs={'property': 'og:title'})['content']  # find the title of the publication
title = title.replace('/', '-')  # replace any backslashes to prevent buggy folder creation

page_url_base = soup.find('meta', attrs={'property': 'og:image'})['content']   # find image url
page_url_base = str(page_url_base).split('_')[0] + '_'

page_count = soup.find_all('script', attrs={"type": "application/javascript"})  # find where pageCount is located
page_count = [page_count[i].contents for i in range(len(page_count)) if "window.__INITIAL_STATE__" in str(page_count[i])]

n_pages = re.findall('"pageCount":[0-9]+', str(page_count))[0]  # find the numbers in page_count
n_pages = n_pages.split(":")[1]  # isolate the number of pages

document = {}  # create dictionary to hold all the pages (keys) and URL:s (values)
for page_number in range(1, int(n_pages)+1):  # iterate over all pages
    document['page_' + str(page_number)] = page_url_base + str(page_number) + '.jpg'


def create_folder(directory):
    """ Create empty folder in the specified directory"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        pass


def download_image(page_url, file_name, file_path=save_path):
    """ Function to download and store images from the web """
    full_path = file_path + '\\' + title + '\\' + title + ' ' + file_name + '.jpg'  # specify file path to store images
    urllib.request.urlretrieve(page_url, full_path)  # download and store images locally


create_folder(save_path + '\\' + title)  # create empty folder in the specified save_path to store images in

for page, url in document.items():
    download_image(url, page)  # iterate over all the elements in the document

print('Done!')
