#!/usr/bin/python

# coding = utf-8

# Created: 2017/03/13 17:22:26
# Implement basic function

# Updated: 2017/03/29 15:18:43
# Fix some bugs. Optimize and refactor code.

# Updated: 2017/03/31 18:04:35
# Fix bug: the number of page maybe small.
# Optimize: make the process of crawling urls faster!

import peewee
from bs4 import BeautifulSoup
import requests
import os
import os.path
import sys
import subprocess
import re

DATABASE_NAME = 'wallpapers'
USERNAME = 'repl'
PASSWORD = 'slackware'


class Wallpaper(peewee.Model):
    id = peewee.PrimaryKeyField()
    url = peewee.CharField(unique=True)
    # pageurl is the webpage which contains the picture
    pageurl = peewee.CharField(default="")
    filename = peewee.CharField()
    filesize = peewee.IntegerField(default=0)
    category = peewee.CharField()
    pop_resolution = peewee.CharField()
    downloaded = peewee.BooleanField()

    class Meta:
        database = peewee.MySQLDatabase(
            DATABASE_NAME, user=USERNAME, passwd=PASSWORD)


def handle_exception(url, proxy=None):
    try:
        if proxy:
            rr = requests.get(url, proxies=proxy)
        else:
            rr = requests.get(url)
        return rr
    except:
        return None


def process_div(div, proxy, all_urls, cnt, category, resolution):
    url = 'http:' + div.find('a').get('href')

    if url in all_urls:
        return None, None

    u1, u2 = re.split('/download/', url, maxsplit=1)
    img_url = u1 + '/image/' + re.sub('/', '_', u2) + '.jpg'
    wallpaper, created = Wallpaper.get_or_create(
        url=img_url,
        filename=os.path.basename(img_url),
        category=category,
        pop_resolution=resolution,
        downloaded=False,
        pageurl=url)
    cnt += 1
    print(category, cnt, img_url)

    if created:
        wallpaper.save()
        all_urls.append(img_url)

    return all_urls, cnt


def iterate_pages(pages_num, cnt, threshold, main_url, proxy, category,
                  all_urls, resolution):
    for page in range(pages_num):
        if cnt >= threshold or Wallpaper.select().where(
                Wallpaper.category == category,
                Wallpaper.pop_resolution == resolution).count() >= threshold:
            break
        p = page + 1
        url = main_url
        url = url if p == 1 else url + '/page' + str(p)
        r = handle_exception(url, proxy)
        if not r:
            continue
        soup = BeautifulSoup(r.content, 'html5lib')
        divs = soup.find('div', class_='wallpapers')

        for div in divs:
            if cnt >= threshold:
                break
            cnt_ = cnt
            _all_urls, cnt = process_div(div, proxy, all_urls, cnt, category,
                                         resolution)
            cnt = cnt_ if not cnt else cnt
            all_urls = _all_urls if _all_urls else all_urls


# crawl a category
def crawl_urls(category, threshold, resolution, use_proxy):
    if use_proxy:
        proxy = {
            'socks5': 'socks5://127.0.0.1:1080',
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
    else:
        proxy = None

    main_url = 'http://wallpaperscraft.com/catalog/' + category \
               + '/' + resolution

    r = handle_exception(main_url, proxy)

    if not r:
        print("Error to get category: ", category)
        return

    soup = BeautifulSoup(r.content, 'html5lib')
    pages = soup.find('div', class_='pages')
    # Fix bug: maybe the number of pages is small. :(
    a_s = pages.find_all("a")
    last_pos = 5 if len(a_s) == 5 else len(a_s)
    pages_num = int(pages.select("a:nth-of-type(%d)" % last_pos)[0].string)

    all_pageurls = [
        wall.pageurl
        for wall in Wallpaper.select()
        .where(Wallpaper.category == category, Wallpaper.pop_resolution ==
               resolution)
    ]
    cnt = len(all_pageurls)
    iterate_pages(pages_num, cnt, threshold, main_url, proxy, category,
                  all_pageurls, resolution)


def crawl(categories, threshold, resolution, use_proxy):
    for category in categories:
        print('-' * 20, '{:^12}'.format(category), '-' * 20)
        if Wallpaper.select().where(
                Wallpaper.category == category,
                Wallpaper.pop_resolution == resolution).count() >= threshold:
            continue
        crawl_urls(category, threshold, resolution, use_proxy)


def download_1image(img_url,
                    img_name,
                    cnt,
                    use_proxy,
                    category,
                    from_db,
                    pic=None):
    print("\n" + "*" * 20 + "{:^15}".format("Downloading") + "*" * 20)
    str_ = "category = {0}\nimg_url = {1}\nimg_name = {2}\ncnt = {3}\n"
    print(str_.format(category, img_url, img_name, cnt + 1))

    if use_proxy:
        cmd = ['proxychains4', 'wget', img_url, '-O', img_name]
    else:
        cmd = ['wget', img_url, '-O', img_name]

    res = subprocess.call(cmd)
    file_size = os.stat(img_name).st_size
    if from_db:
        pic.filesize = file_size

    # remove files whose size is below 90000. It's possibly corrupted.
    if res == 0 and file_size >= 90000:
        if from_db:
            pic.downloaded = True
            pic.save()
        cnt += 1
        return cnt
    else:
        os.remove(img_name)
        return None


def download_from_db(category, resolution, cnt, threshold, dir_path,
                     use_proxy):
    for pic in Wallpaper.select().where(
            Wallpaper.category == category,
            Wallpaper.pop_resolution == resolution).order_by(Wallpaper.id):
        if cnt >= threshold:
            break
        if pic.downloaded:
            cnt += 1
            print("Already downloaded: {0}, category: {1}\n".format(
                cnt, category))
            continue

        _cnt = download_1image(pic.url,
                               os.path.join(dir_path, pic.filename), cnt,
                               use_proxy, category, True, pic)
        cnt = _cnt if _cnt else cnt


def download_from_org(category, resolution, cnt, threshold, dir_path,
                      use_proxy):
    path = os.path.join(os.getcwd(), "urls", resolution)

    if not os.path.exists(path):
        os.exit("Directory not found: " + path)

    file_name = os.path.join(path, category + ".org")

    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            for line in f:
                if cnt >= threshold:
                    break
                url = line.rstrip()
                _cnt = download_1image(url,
                                       os.path.join(dir_path,
                                                    os.path.basename(url)),
                                       cnt, use_proxy, category, False)
                cnt = _cnt if _cnt else cnt


def download_images(path, categories, threshold, resolution, use_proxy,
                    from_db):
    for category in categories:
        cnt = 0
        dir_path = os.path.join(path, category)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if from_db:
            download_from_db(category, resolution, cnt, threshold, dir_path,
                             use_proxy)
        else:
            download_from_org(category, resolution, cnt, threshold, dir_path,
                              use_proxy)


def crawl_main(categories, resolution, pictures_dir, threshold, proxyp):
    path = os.path.join(pictures_dir, resolution)

    if not os.path.exists(path):
        os.makedirs(path)

    crawl(categories, threshold, resolution, proxyp)
    download_images(path, categories, threshold, resolution, proxyp, True)


# export all picture urls to .org text file
def log2file(resolution, all_categories):
    path = os.path.join(os.getcwd(), "urls", resolution)
    if not os.path.exists(path):
        os.makedirs(path)
    for category in all_categories:
        file_name = os.path.join(path, category + ".org")
        urls = [
            wall.url
            for wall in Wallpaper.select()
            .where(Wallpaper.category == category, Wallpaper.pop_resolution ==
                   resolution)
        ]
        exist_urls = []

        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                for line in f:
                    exist_urls.append(line.rstrip())

        print(category)

        with open(file_name, "a+") as f:
            for url in urls:
                if url not in exist_urls:
                    print("Add url: ", url)
                    f.write(url + "\n")


def check_argv(categories, all_categories, pop_resolutions):
    pop_resolutions_str = ', '.join(
        pop_resolutions) + ". Please refer to http://wallpaperscraft.com/ for \
 more supported resolution."

    pictures_dir = os.path.expanduser("~/Pictures/Wallpapers")

    if not os.path.exists(pictures_dir):
        sys.exit("ERROR: directory '{0}' not found".format(pictures_dir))

    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print(
            '''Usage      : python ./Wallpaper_DB.py resolution threshold mode [--proxy]
             python ./Wallpaper_DB.py resolution --logfile

resolution : {0}

threshold  : It is a integer which represents the number of wallpapers you \
want to download for EACH category.

mode       : online or local. online option means the URLS of wallpapers are \
crawled from the Internet if necessary or read directory from the \
Database. local option means the URLS of wallpapers is read from local \
*.org. Note: The *.org files is generated using --logfile option.

--proxy    : If this option is given, the script will use socks5 proxy \
when downloading wallpapers using wget and proxychains. This option is \
optional.

--logfile : This option will export all of the wallpaper URLs of each \
category from the database to .org files and save those files into \
the current directory named `urls`. It assumes your database is not empty.

*Note*: Please update the `categories` variable if necessary. This \
script will download all of the categories by default.

eg.
python Wallpaper_DB.py 1440x900 2 online --proxy
python Wallpaper_DB.py 1440x900 2 online
python Wallpaper_DB.py 1440x900 2 local --proxy
python Wallpaper_DB.py 1440x900 2 local
python Wallpaper_DB.py 1440x900 --logfile'''.format(pop_resolutions_str))
        sys.exit()

    if len(sys.argv) < 3:
        sys.exit(
            "Usage: python ./Wallpaper_DB.py resolution threshold [-proxy]\n" +
            "Popular resolutions are: " + pop_resolutions_str)

    resolution = sys.argv[1]

    if len(sys.argv) == 3:
        if (sys.argv[2] == "--logfile"):
            log2file(resolution, all_categories)
    elif len(sys.argv) >= 4:
        proxyp, threshold = None, int(sys.argv[2])

        if len(sys.argv) > 4 and sys.argv[4] == "--proxy":
            proxyp = True

        if sys.argv[3] == "online":
            crawl_main(categories, resolution, pictures_dir, threshold, proxyp)
        elif sys.argv[3] == "local":
            download_images(
                os.path.join(pictures_dir, resolution), categories, threshold,
                resolution, proxyp, False)


if __name__ == '__main__':
    Wallpaper.create_table(fail_silently=True)

    pop_resolutions = [
        '1366x768', '1920x1080', '360x640', '1024x768', '1600x900', '1280x900',
        '1440x900', '1280x1024', '800x600', '1680x1050', '2560x1440',
        '320x480', '1920x1200', '480x800', '720x1280'
    ]

    all_categories = [
        '3d', 'anime', 'abstract', 'animals', 'city', 'fantasy', 'flowers',
        'food', 'games', 'girls', 'hi-tech', 'holidays', 'macro', 'men',
        'movies', 'music', 'nature', 'other', 'space', 'sport', 'textures',
        'tv-series', 'vector'
    ]
    # categories = ['games', 'hi-tech']
    categories = all_categories
    check_argv(categories, all_categories, pop_resolutions)
