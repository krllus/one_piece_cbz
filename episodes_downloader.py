#!/usr/bin/env python3
# create onepice manga .cbz file

import requests
import json
import os
import sys
import subprocess
from bs4 import BeautifulSoup
from html.parser import HTMLParser


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_pages_for_episode(episode):
    # download page from url
    url_base = "https://onepieceex.net/mangas/leitor/{}"
    manga_url_base = "https://onepieceex.net/{}"

    episode_url = url_base.format(episode)

    site = get_page(episode_url).prettify()

    site_html = site.splitlines()
    
    try:
        manga_page_list_as_string = [
            line for line in site_html if 'paginasLista = "{' in line][0]
        manga_page_list_as_string = manga_page_list_as_string.replace(
            "\tpaginasLista = \"", "").replace('\\', "").replace('";', "")
        manga_page_list_as_json = json.loads(manga_page_list_as_string)
    except Exception:
        manga_page_list_as_json = {}
    pages = []

    for key in manga_page_list_as_json.keys():
        pages.append(manga_url_base.format(manga_page_list_as_json[key]))

    return pages


def create_episode_path(episode):
    current_dir = os.getcwd()
    episode_folder_path = os.path.join(current_dir, "downloads")
    episode_folder_path = os.path.join(episode_folder_path, str(episode))
    os.makedirs(episode_folder_path, exist_ok=True)
    return episode_folder_path


def download_pages(episode, pages):
    episode_folder_path = create_episode_path(episode)
    for page in pages:
        filename = page.split("/")[-1]
        filename_path = os.path.join(episode_folder_path, filename)
        download_page(page, filename_path)


def download_page(url, filename):
    print("Downloading: " + url)
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)


def compact_folder(episode):
    episode_folder_path = create_episode_path(episode)
    episode_file = "onepiece_" + str(episode) + ".cbz"
    episode_file_path = os.path.join(episode_folder_path, episode_file)
    subprocess.call(["zip", "-r", episode_file_path, episode_folder_path])


def main(argv):
    episode_list = []

    if (len(argv) == 1):
        try:
            eposide_number = int(argv[0])
            if eposide_number <= 0:
                raise AttributeError("Sorry, no numbers below zero")
            episode_list.append(eposide_number)
        except ValueError:
            print(
                'Episode number is not valid! try again. your input: {}'.format(argv[0]))
        except AttributeError as ex:
            print(ex)

    for episode in episode_list:
        pages = get_pages_for_episode(episode)
        if(len(pages) == 0):
            print('episode #{} not found!'.format(episode))
            continue
        download_pages(episode, pages)
        compact_folder(episode)
        print("download episode completed: " + str(episode))


if __name__ == "__main__":
    main(sys.argv[1:])
