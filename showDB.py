import tkinter as tk
import sqlite3
import WillsLib
# This is the version as of 7-20-14, commit hash 3f5c782b8523602173ef649cd55452627ae9155e
class DBRow(tk.Frame):
	def __init__(self, root, row_index, name):
		self.frame = tk.Frame(root)
		tk.Label(self.frame, text=name).pack()
		list = tk.ListBox(self.frame)
		list.pack()
		# Make methods to put stuff in the list. 
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name):
		self.connection = connection
		columns = []
		self.table_name = table_name
		self.column_names = [i[1] for i in self.connection.cursor().execute("pragma table_info(%s)" % self.table_name)]
		main_frame = tk.Frame(root)
		for i, j in enumerate(column_names):
			columns.append(DBRow(self.main_frame, j, i))
			columns[-1].pack(side='left')
def showDB(db_location):
	db = sqlite3.connect(db_location)
	c = db.cursor()
	
if True: # Change this to be if it's opened as it's own program, so it doesn't run if imported. 
	showDB("test.db")
