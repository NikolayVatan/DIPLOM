import os
import requests
import sys
import re
import pymongo
from pymongo import MongoClient
import datetime
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = '5de64958c0c444d7b08081bc887c21fd'
os.environ['SPOTIPY_CLIENT_SECRET'] = '97d43cc07514498c90de99b77e80b6d0'


def check_mongo(query, limit=25):  ##Проверяет есть ли файлы в монго
    client = MongoClient()
    db = client.giphy
    collection = db.giphy
    link = collection.find_one({'request': query})  ##Название
    if link and (len(link["urls"])) == limit:
        print("returning")
        return link
    return None


def write_to_mongo(giphname, to_write):  ##Записывает в монго
    client = MongoClient()
    db = client.giphy
    collection = db.giphy
    mp4links = {
        'request': giphname,
        'urls': to_write
    }
    post_id = collection.insert_one(mp4links).inserted_id


def search(giphname, limit=25):  ## Поиск файлов в интернет

    sess = requests.Session()
    url2 = 'https://api.giphy.com/v1/gifs/search?api_key=nPkN0MiAw2VxnVVGtZ7bwp3hFfFbQYFN&limit=' + str(limit) + \
           '&q=' + \
           giphname
    rs = sess.get(url2)
    links = rs.json()['data']
    try:
        os.mkdir(path='/home/vatan/PycharmProjects/giphyckeck/' + giphname)  # создет папку для скачивамых видео с
        # названием запроса
    except:
        pass
    resultsmp4link = []
    for link in links:
        res = (link['images']['original_mp4']['mp4'])
        resultsmp4link.append(res)
        print(res)
        filename = re.search('https://media.*\\.giphy\\.com/media/([a-zA-Z0-9]*)/', res).group(1)
        rsf = sess.get(res)
        with open('/home/vatan/PycharmProjects/giphyckeck/' + giphname + '/' + filename + '.mp4', 'wb') as f:
            f.write(rsf.content)  # Скачивает видеозаписи по ссылкам
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())  ## Музыка
    results = sp.search(q="Good", limit=5)
    trackend = []
    for idx, track in enumerate(results['tracks']['items']):
        print(track['external_urls']['spotify'])
        trackend.append(track['external_urls']['spotify'])
    return resultsmp4link, trackend


def main(query, limit):
    if len(sys.argv) == 1:
        mongo_contents = check_mongo(query, limit)
        if mongo_contents:
            pass
        else:
            found = search(query)
            write_to_mongo(query, found)


# main(*(("Russia", 25) if __name__ == "__main__" else sys.argv[1:3]))
if __name__ == '__main__':
    if len(sys.argv) == 1:
        mongo_contents = check_mongo(query="Russia", limit=25)
        if mongo_contents:
            pass
        else:
            found = (search(giphname="Russia", limit=25))
            write_to_mongo(search(giphname="Russia"), found)
    else:
        print(search(giphname=sys.argv[1], limit=sys.argv[2]))
