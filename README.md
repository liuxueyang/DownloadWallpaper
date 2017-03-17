# DownloadWallpaper
Download wallpapers from http://wallpaperscraft.com/

## Notes

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

+----------------+------------------+------+-----+---------+----------------+
| Field          | Type             | Null | Key | Default | Extra          |
+----------------+------------------+------+-----+---------+----------------+
| id             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| url            | varchar(255)     | NO   | UNI | NULL    |                |
| filename       | varchar(255)     | NO   |     | NULL    |                |
| category       | varchar(255)     | NO   |     | NULL    |                |
| pop_resolution | varchar(255)     | NO   |     | NULL    |                |
| downloaded     | tinyint(1)       | NO   |     | NULL    |                |
| filesize       | int(11)          | NO   |     | 0       |                |
| pageurl        | varchar(255)     | NO   |     |         |                |
+----------------+------------------+------+-----+---------+----------------+

![Wallpaper folder](http://wstaw.org/m/2017/03/17/plasma-desktopqj1799.png)
