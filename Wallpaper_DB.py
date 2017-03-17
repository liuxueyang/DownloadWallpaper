#!/usr/bin/python

# coding = utf-8

# 2017/03/13 17:22:26

import peewee
from peewee import *
from bs4 import BeautifulSoup
import requests
import urllib
import os
import os.path
import subprocess
import re


class Wallpaper(peewee.Model):
    id = peewee.PrimaryKeyField()
    url = peewee.CharField(unique = True)
    pageurl = peewee.CharField(default = "")
    filename = peewee.CharField()
    filesize = peewee.IntegerField()
    category = peewee.CharField()
    pop_resolution = peewee.CharField()
    downloaded = peewee.BooleanField()

    class Meta:
        database = MySQLDatabase('wallpapers', user = 'repl', passwd = 'slackware')


def handle_exception(url, proxy):
    try:
        rr = requests.get(url, proxies = proxy)
        return rr
    except:
        return None


def process_div(div, proxy, all_urls, cnt, all_pageurls, category):
    url = 'http:' + div.find('a').get('href')
    if url in all_pageurls: return None
    rr = handle_exception(url, proxy)
    if not rr: return None
    ss = BeautifulSoup(rr.content, 'html5lib')
    a_tag = ss.find('a', class_='wd_zoom')

    if a_tag is not None:
        img_url = a_tag.img.get('src')
        img_url = 'http:' + img_url
        wallpaper, created = Wallpaper.get_or_create(url = img_url, filename = os.path.basename(img_url), category = category, pop_resolution = '1366x768', downloaded = False, pageurl = url)
        if created:
            cnt += 1
            wallpaper.save()
            print category, cnt, img_url
            all_urls.append(img_url)

    return all_urls


def iterate_pages(pages_num, cnt, threshold, main_url, proxy, category, all_urls):
    all_pageurls = [wall.pageurl for wall in Wallpaper.select().where(Wallpaper.category == category, Wallpaper.pageurl != "")]

    for page in range(pages_num):
        if cnt >= threshold or Wallpaper.select().where(Wallpaper.category == category).count() >= threshold: break
        p = page + 1
        url = main_url
        url = url if p == 1 else url + '/page' + str(p)
        r = handle_exception(url, proxy)
        if not r: continue
        soup = BeautifulSoup(r.content, 'html5lib')
        divs = soup.find('div', class_='wallpapers')

        for div in divs:
            _all_urls = process_div(div, proxy, all_urls, cnt, all_pageurls, category)
            all_urls = _all_urls if _all_urls else all_urls


# craw a category
def crawl_urls(category, threshold, resolution):
    proxy = { 'socks5' : 'socks5://127.0.0.1:1080',
          'http' : 'socks5://127.0.0.1:1080',
          'https' : 'socks5://127.0.0.1:1080'}
    main_url = 'http://wallpaperscraft.com/catalog/' + category + '/' + resolution

    r = handle_exception(main_url, proxy)
    if not r:
        print "Error to get category: ", category
        return

    soup = BeautifulSoup(r.content, 'html5lib')
    pages = soup.find('div', class_='pages')
    pages_num = int(pages.select("a:nth-of-type(5)")[0].string)
    all_pageurls = [wall.pageurl for wall in Wallpaper.select().where(Wallpaper.category == category)]
    cnt = len(all_pageurls)
    iterate_pages(pages_num, cnt, threshold, main_url, proxy, category, all_pageurls)


def crawl(categories, threshold, resolution):
    for category in categories:
        print "------", category
        if Wallpaper.select().where(Wallpaper.category == category).count() >= threshold:
            continue
        crawl_urls(category, threshold, resolution)


def filename2pageurl(filename):
    url = 'http://wallpaperscraft.com/download/'
    filename = re.split('\.', filename)[0]
    resolution = re.split('_', filename)[-1]
    path = '_'.join(re.split('_', filename)[:-1])
    return url + path + '/' + resolution


def insert_page_url():
    for pic in Wallpaper.select().where(Wallpaper.pageurl == ""):
        pic.pageurl = filename2pageurl(pic.filename)
        pic.save()
        print pic.id, pic.pageurl


def check_page_url():
    resolution = '1366x768'

    for pic in Wallpaper.select().where(Wallpaper.pageurl != ""):
        if not pic.pageurl.endswith(resolution):
            print pic.id, pic.pageurl



def download_1image(img_url, img_name, pic, cnt):
    # cmd = ['proxychains4', 'wget', img_url, '-O', img_name]
    cmd = ['wget', img_url, '-O', img_name]
    # subprocess.Popen(cmd).wait()
    re = subprocess.call(cmd)
    
    # cmd_str = 'wget ' + img_url + ' -O ' + img_name
    # os.system(cmd_str)
        
    # f = open(img_name, 'wb')
    # f.write(requests.get(img_url).content)
    # f.close()

    file_size = os.stat(img_name).st_size
    pic.filesize = file_size

    print "\n" + "*" * 10 + "\n" + "file_size = {0}\nIn Function, cnt = {1}\nre = {2}\n".format(file_size, cnt, re) + "\n" + "*" * 10 + "\n"

    if re == 0 and file_size >= 100000:
        pic.downloaded = True
        pic.save()
        cnt += 1
        return cnt
    else:
        os.remove(img_name)
        return None


def download_images(path, categories, threshold):
    for category in categories:
        cnt = 0
        dir_path = os.path.join(path, category)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for pic in Wallpaper.select().where(Wallpaper.category == category).order_by(Wallpaper.id):
            if cnt >= threshold: break
            if pic.downloaded:
                cnt += 1
                print "Already downloaded: {0}, category: {1}\n".format(cnt, category)
                continue
            
            img_url = pic.url
            img_name = os.path.join(dir_path, pic.filename)

            print "\n" + "*" * 10 + "\n" + "category = {0}\nimg_url = {1}\nimg_name = {2}\ncnt = {3}\n".format(category, img_url, img_name, cnt) + "*" * 10 + "\n"
            # i__ = raw_input()

            _cnt = download_1image(img_url, img_name, pic, cnt)
            cnt = _cnt if _cnt else cnt


if __name__ == '__main__':
    Wallpaper.create_table(fail_silently = True)

    categories = ['3d', 'anime', 'abstract', 'animals', 'city', 'fantasy', 'flowers', 'food', 'games', 'girls', 'hi-tech', 'holidays', 'macro', 'men', 'movies', 'music', 'nature', 'other', 'space', 'sport', 'textures', 'tv-series', 'vector']
    threshold = 100
    resolution = '1366x768'
    path = '/home/repl/Pictures/Wallpapers/All'

    # insert_page_url()
    # check_page_url()
    crawl(categories, threshold, resolution)
    download_images(path, categories, threshold)
