下载壁纸
==========

壁纸来源：http://wallpaperscraft.com/

### 选项

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

### 说明

1. 数据库使用MySQL，数据库名称：`wallpapers`，用户名：`repl`，数据库密码：`slackware`，根据需要在程序的开头更改。
2. 目录`urls`里面已经包含了我爬取的分辨率为`1366x768`的总共10704张壁纸的地址，可在不需要数据库的情况下可以直接下载壁纸。
3. 依赖：refer to `requirements.txt`。如果需要使用代理，需要`proxychains4`。只支持Python2，不支持Python3。

![Wallpaper folder](http://wstaw.org/m/2017/03/17/plasma-desktopqj1799.png)

### 更新

#### 2017/03/31

在`urls`目录中增加2300张分辨率为`1440x900`的壁纸下载地址，按照类别存放在不同的`*.org`文件里。

修复一个bug：某个类别的壁纸页数可能很少。

优化爬取地址的逻辑，不必对每张图片都请求一次页面，直接用正则从链接拼出图片所在的
页面和图片的地址。这样爬取过程就快很多，请求页面的次数等于壁纸的「页数」。每页大
概有15张壁纸。

#### 2018/03/27

使用 `argparse` 重构命令行接口。
