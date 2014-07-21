import tkinter as tk
import sqlite3
import WillsLib
# This is the version of WillsLib as of 7-20-14, commit hash 3f5c782b8523602173ef649cd55452627ae9155e
# In 2.4, there is iteritems(), in 3 there is just items(). *sigh*
class DBColumn(tk.Frame):
	def __init__(self, root, name):
		tk.Frame.__init__(self, root)
		self.name = name
		tk.Label(self, text=name).pack()
		list = tk.ListBox(self.frame)
		list.pack()
		self.curselection = self.list.curselection
		self.config = self.list.config
		self.insert = self.list.insert
		# Make methods to put stuff in the list. 
		# Also, how to I access the tk.Frame methods?
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name):
		self.connection = connection
		columns = {}
		self.table_name = table_name
		self.column_names = [i[1] for i in self.connection.cursor().execute("pragma table_info(%s)" % self.table_name)]
		tk.Frame.__init__(self, root)
		for i, j in enumerate(column_names):
			columns[j] = (DBColumn(self, i))
			columns[j].pack(side='left')
	def add(self, cols):
		# Cols is a dictionary.
		if len(columns) != len(cols):
			raise Exception("You didn't give the right amount of columns!")
		else:
			for i, j in items(cols):
				columns[i].insert('end', j)
	def populate(self):
		rows = WillsLib.DBselect(self.connection, self.table_name, 'all', 'all')
		row_dictionary = {}
		for i, j in enumerate(rows):
			self.add({column_names[h]:k for h, k in enumerate(j)})
def showDB(db_location):
	db = sqlite3.connect(db_location)
	c = db.cursor()
	
if True: # Change this to be if it's opened as it's own program, so it doesn't run if imported. 
	showDB("test.db")
