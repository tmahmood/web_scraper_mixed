Installation
============
You need latest version of (Python 3)[https://www.python.org/downloads/]

Once installed, open command prompt and  execute the followings to install other
required files

    py -m pip install lxml requests cssselect

(Sqlitebrowser)[http://sqlitebrowser.org/] is also required to view the data

That's all!

How to execute the application
==============================

open cmd prompt in the application folder,
  1. Open the application folder in File explorer
  2. Click on the empty space in the addressbar
  3. Type: cmd<Enter>

this should open up a command prompt window, Now The application can be executed by
the following commands:

## SEEK
    py app.py seek "<keyword>"

## GUMTREE
    py app.py gumtree "<keyword>"

The command will continue to download until end of the results are reached, data
will be available in corrosponding sqlite database files. Word of caution: If too
many hits made the sites can block you. for that I've added 3 seconds timeout for
every 10 links downloaded, which may not be enough.

You can terminate the script anytime using Ctrl+Break in windows, all data before
current page will be saved.

to reset the data (which should not be needed normally) you just need to delete the
corrosponding database file

for `seek` data will be stored in `seek.db`
for `gumtree` data will be stored in `gumtree.db`

Sqlite database files can be opend with (sqlitebrowser)[http://sqlitebrowser.org/],
with the application you can export the data as csv/xml/json files

Any question you can always ask me on fivrr :)
