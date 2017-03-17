# DownloadWallpaper
Download wallpapers from http://wallpaperscraft.com/

## Notes

## How it works

1. It crawls the URL of those wallpapers and store them into the database.
2. Download wallpapers using URLS from database and store them to target directory.

### Some variables to customize

- categories: Those categories you are interested in. It includes all by default.
- threshold: The number of wallpapers to download in each category.
- resolution: The resultion of you computer.
- path: The directory to store all of the folds of each category.

### Database Configruation

- Database name: wallpapers
- Database user: repl
- Database password: slackware
- The only table in `wallpapers`: wallpaper
- Table info

![Table info](http://wstaw.org/m/2017/03/17/plasma-desktopJn1799.png)

![Wallpaper folder](http://wstaw.org/m/2017/03/17/plasma-desktopqj1799.png)
