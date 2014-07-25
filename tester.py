import showDB
import WillsLib
import sqlite3

db = sqlite3.connect("test.db")
# WillsLib.DBcreate(db, "test", ['alpha', 'beta', 'gamma', 'delta'])
# WillsLib.DBinsert(db, 'test', ['Freddy', 'Johnny', 'Anna', 'George'])
# WillsLib.DBinsert(db, 'test', ['Amy', 'Andy', 'David', 'Mark'])
# WillsLib.DBinsert(db, 'test', ['Tom', 'Ron', 'Zack', 'Lennie'])
# WillsLib.DBinsert(db, 'test', ['Jack', 'Andrew', 'Reginald', 'Mel'])
showDB.showDB('test.db', 'test')