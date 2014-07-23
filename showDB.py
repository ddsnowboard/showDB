import tkinter as tk
import sqlite3
import WillsLib
# This is the version of WillsLib as of 7-20-14, commit hash 3f5c782b8523602173ef649cd55452627ae9155e
# In 2.4, there is iteritems(), in 3 there is just items(). *sigh*
class DBColumn(tk.Frame):
	def __init__(self, root, name, index):
		# Add the command to select all the other columns when you click one. 
		tk.Frame.__init__(self, root, command=
		self.name = name
		self.index = index
		tk.Label(self, text=name).pack()
		list = tk.Listbox(self)
		list.pack()
		self.curselection = list.curselection
		self.config = list.config
		self.insert = list.insert
		# Make methods to put stuff in the list. 
		# Also, how to I access the tk.Frame methods?
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name):
		self.connection = connection
		self.columns = {}
		self.table_name = table_name
		self.column_names = [i[1] for i in self.connection.cursor().execute("pragma table_info(%s)" % self.table_name)]
		tk.Frame.__init__(self, root)
		for i, j in enumerate(self.column_names):
			self.columns[j] = (DBColumn(self, j, i))
			self.columns[j].pack(side='left')
		self.populate()
	def add(self, cols):
		# Cols is a dictionary.
		if len(self.columns) != len(cols):
			raise Exception("You didn't give the right amount of columns!")
		else:
			for i, j in cols.items():
				self.columns[i].insert('end', j)
	def populate(self):
		rows = WillsLib.DBselect(self.connection, self.table_name, 'all', 'all')
		row_dictionary = {}
		for i, j in enumerate(rows):
			self.add({self.column_names[h]:k for h, k in enumerate(j)})
def showDB(db_location, table_name):
	global DB
	db = sqlite3.connect(db_location)
	c = db.cursor()
	root = tk.Tk()
	DB = DBList(root, db, table_name)
	DB.pack()
	root.mainloop()
	
if True: # Change this to be if it's opened as it's own program, so it doesn't run if imported.
	db = sqlite3.connect('test.db')
	c = db.cursor()
	showDB("test.db", 'test')