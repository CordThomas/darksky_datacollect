Using https://github.com/lukaskubis/darkskylib, pull current
atmospheric conditions for my home location to store in a local database.

Install the DarkSkyLib via:  pip install darkskylib

The code relies on the existence of a params.py file located in the running users
home directory (/home/pi or /root/ in my case).   I maintain these configs
in a separate repository that is private.  The strucutre in this case is:

[DARKSKY]
# DarkSky API key - retrieved here:  https://darksky.net/dev/register
darksky_api_key = f0617.....00394
# Location of our sqlite3 DB to store the darksky parameters for my home
db_location = /mnt/usb1/darksky/darksky.db

It also relies on the coordinate configuration i supplied to Open Weather Map, so
those are in:

[OPEN_WEATHERMAP]
own_coord_lat = 33.NNNNNN
own_coord_long = -118.NNNNNN

Database structure is pretty self explanatory. There's no real need to
separate the date and time fields; i just do it out of convention.

CREATE TABLE darksky (
tdateTEXT,
ttimeTEXT,
paramTEXT,
valTEXT
);