import showDB
import WillsLib
import sqlite3

db = sqlite3.connect("test.db")
WillsLib.DBcreate(db, "nums", ['n1', 'n2', 'n3'])
WillsLib.DBinsert(db, 'nums', [3, 5, 7])
showDB.showDB('test.db', 'nums')