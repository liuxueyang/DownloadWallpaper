下载壁纸
==========

壁纸来源：http://wallpaperscraft.com/

### 选项

```
Usage      : python ./Wallpaper_DB.py resolution threshold mode [--proxy]
             python ./Wallpaper_DB.py resolution --logfile
	     python ./Wallpaper_DB.py -h

resolution : 1366x768, 1920x1080, 360x640, 1024x768, 1600x900, 1280x900, 1440x900, 1280x1024, 800x600, 1680x1050, 2560x1440, 320x480, 1920x1200, 480x800, 720x1280. Please refer to http://wallpaperscraft.com/ for  more supported resolution.

threshold  : It is a integer which represents the number of wallpapers you want to download for EACH category.

mode       : online or local. online option means the URLS of wallpapers are crawled from the Internet if necessary or read directory from the Database. local option means the URLS of wallpapers is read from local *.org. Note: The *.org files is generated using --logfile option.

--proxy    : If this option is given, the script will use socks5 proxy when downloading wallpapers using wget and proxychains. This option is optional.

--logfile : This option will export all of the wallpaper URLs of each category from the database to .org files and save those files into the current directory named `urls`. It assumes your database is not empty.

*Note*: Please update the `categories` variable if necessary. This script will download all of the categories by default.

eg.
python Wallpaper_DB.py 1440x900 2 online --proxy
python Wallpaper_DB.py 1440x900 2 online
python Wallpaper_DB.py 1440x900 2 local --proxy
python Wallpaper_DB.py 1440x900 2 local
python Wallpaper_DB.py 1440x900 --logfile

```

### 说明

1. 在`__main__`里根据自己的需要更改`categories`来指定自己想要爬取的壁纸类别。
2. 数据库使用MySQL，数据库名称：`wallpapers`，用户名：`repl`，数据库密码：`slackware`，根据自己的需要在程序里面更改。
3. 目录`urls`里面已经包含了我爬取的分辨率为`1366x768`的总共10704张壁纸的地址，可以直接使用，在不需要数据库的情况下可以直接下载壁纸（每个类别下载2张）：

```
python Wallpaper_DB.py 1440x900 2 local
```

或者使用代理：

```
python Wallpaper_DB.py 1440x900 2 local --proxy
```

4. 依赖：`peewee`，`BeautifulSoup`，`requests`，`wget`。如果需要使用代理，需要`proxychains4`。

![Wallpaper folder](http://wstaw.org/m/2017/03/17/plasma-desktopqj1799.png)
