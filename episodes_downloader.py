#!/usr/bin/env python3
# create onepice manga .cbz file

import requests
import json
import os
import re
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

def get_chapters_list():
    # download page from url
    url_chapters = "https://onepieceteca.com/ler-online/manga-one-piece/ajax/chapters/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.post(url_chapters, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def build_episode_pages(manga_id, episode_id, page_count):
    episode_page_base_url = "https://onepieceteca.com/wp-content/uploads/WP-manga/data/{}/{}/{}.jpg"
    
    episode_pages_url = []
    
    try:
        max_range = int(page_count) + 1
        for page in range(1, max_range, 1):
            page_formated = "{0:0=2d}".format(page)
            episode = episode_page_base_url.format(manga_id, episode_id, page_formated)
            episode_pages_url.append(episode)
    except:
        pass    

    return episode_pages_url

def get_pages_for_episode_url(episode_url):
    print(episode_url)
    
    manga_page = get_page(episode_url)
    
    manga_features = manga_page.find_all('img', class_='wp-manga-chapter-img')
    manga_identification = manga_features[0].get("data-src").split("/")
    manga_identification.reverse()
    
    manga_id = manga_identification[2]
    episode_id = manga_identification[1]
    page_count = 0
    
    options = manga_page.find_all('option')
    for option in options:
        option_selected = option.get("selected") == "selected"
        option_value_1 = option.get("value") == "1"
        option_data_redirect_not_null = option.get("data-redirect") is not None
        if(option_selected and option_value_1 and option_data_redirect_not_null):
            page_count = option.text.split("/")[-1]
    
    return build_episode_pages(manga_id, episode_id, page_count)

def get_episode_url(chapters, episode):
    found_url = None
    for chapter in chapters:
        
        if chapter["id"].casefold() == str(episode).casefold():
            found_url = chapter["href"]
            break
    return found_url

def get_all_chapters(offline):
    
    if(offline):
        with open("all_chapters.json", "r") as file:
            json_string = file.read()
            json_data = json.loads(json_string)
            return json_data
    
    soup = get_chapters_list()    
    try:
        chapters = soup.find_all('li', class_='wp-manga-chapter')        
        
        chapters_list = []
        
        for chapter in chapters:
            chapter_link = chapter.find('a')
            href = chapter_link.get('href')
            text = chapter_link.text.strip()
            episode = re.sub(r'\D', '', text)  # \D matches any non-numeric character
            chapters_list.append({"id": episode,"text": text, "href": href})
        
        with open("all_chapters.json", "w") as json_file:
            json_string = json.dumps(chapters_list)
            json_file.write(json_string)
        
    except Exception:
        chapters_list = []
    return chapters_list
    

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    print("Downloading: " + url)
    page = requests.get(url, headers=headers)
    open(filename, 'wb').write(page.content)


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

    
    chapters = get_all_chapters(True)
    
    for episode in episode_list:
        
        episode_url = get_episode_url(chapters=chapters, episode=episode)
        if(episode_url == None):
            print('episode url #{} not found!'.format(episode))
            continue
        
        pages = get_pages_for_episode_url(episode_url)
        if(len(pages) == 0):
            print('no pages found for episode #{}!'.format(episode))
            continue
        download_pages(episode, pages)
        compact_folder(episode)
        print("download episode completed: " + str(episode))


if __name__ == "__main__":
    main(sys.argv[1:])
