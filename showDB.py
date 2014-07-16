import tkinter as tk
import sqlite3
def showDB(db_location):
	db = sqlite3.connect(db_location)
	c = db.cursor()
	
if True: #Change this to be if it's opened as it's own program, so it doesn't run if imported. 
	showDB("test.db")
