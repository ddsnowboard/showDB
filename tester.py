# This is just to test using showDB as an external library. 

import showDB
import WillsLib
import sqlite3

db = sqlite3.connect("test.db")
# WillsLib.DBcreate(db, "test2", ['name', 'date', 'location'])
# WillsLib.DBinsert(db, 'test2', ['Freddy', '9-16-12', 'France'])
# WillsLib.DBinsert(db, 'test2', ['Amy', '5-22-12', 'Germany'])
# WillsLib.DBinsert(db, 'test2', ['Tom', '3-21-13', 'Romania'])
showDB.showDB('test.db', 'test2', ['date', 'name', 'location'])