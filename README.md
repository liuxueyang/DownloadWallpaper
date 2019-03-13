Download Wallpaper

----

Download Wallpapers from: http://wallpaperscraft.com/

### Help

``` shell
usage: downloadbg.py [-h] [--resolution RESOLUTION]
                     [--category [CATEGORY [CATEGORY ...]]] [--num NUM]
                     [--mode {online,local}] [--proxy] [--log]

download different types of wallpaper from http://wallpaperscraft.com and save
them to directory `~/Pictures/Wallpapers`.

optional arguments:
  -h, --help            show this help message and exit
  --resolution RESOLUTION
                        Optional resolutions are: 1366x768, 1920x1080,
                        360x640, 1024x768, 1600x900, 1280x900, 1440x900,
                        1280x1024, 800x600, 1680x1050, 2560x1440, 320x480,
                        1920x1200, 480x800, 720x1280
  --category [CATEGORY [CATEGORY ...]]
                        Optional categories are: 3d, anime, abstract, animals,
                        city, fantasy, flowers, food, games, girls, hi-tech,
                        holidays, macro, men, movies, music, nature, other,
                        space, sport, textures, tv-series, vector. Default
                        option is: all.
  --num NUM             count of wallpapers to download for each category.
  --mode {online,local}
                        online: crawl urls of wallpapers from
                        http://wallpaperscraft.com or get from database;
                        local: read urls from `org` files in `urls` directory;
                        NOTE: `org` files can be generated using `--log`
                        option.
  --proxy               use proxychains to download or crawl wallpapers urls.
  --log                 export all of the wallpaper urls of specified
                        resolution in database to org files in directory named
                        `urls`
```

### About

1. MySQL Configuration: `cp config.sample.json config.json`.
2. There are some generated Wallpaper URLs in urls directory.
3. Use socks5 proxy if enabled.

### TODO

Refactor and optimize this script

- [ ] add comment for functions
- [ ] add multithread support
- [X] download files using python library instead of `wget`
- [X] put database username and password into environment variables

### Updates

#### 2017/03/31

在`urls`目录中增加 2300 张分辨率为`1440x900`的壁纸下载地址，按照类别存
放在不同的`*.org`文件里。

修复一个 bug：某个类别的壁纸页数可能很少。

优化爬取地址的逻辑，不必对每张图片都请求一次页面，直接用正则从链接拼出
图片所在的页面和图片的地址。这样爬取过程就快很多，请求页面的次数等于壁
纸的「页数」。每页大概有 15 张壁纸。

#### 2018/03/27

refactor argument interface using `argparse` package.

#### 2018/12/09

- Update code according to new site.
- move database configuration to `config.json` file.
- update packages in requirements.txt
- Migrate to Python3

#### 2018/12/10

- use `urllib.request` to download files and `progressbar` to show
  progress.
- add widgets to progress bar

#### 2018/12/19

- update requirements.txt
- move proxy PORT to configuration

#### 2019/03/13

- set proxy option default to be false
- fix bug: rename page_url field
