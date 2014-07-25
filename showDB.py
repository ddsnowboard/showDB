import tkinter as tk
import sqlite3
import WillsLib
# This is the version of WillsLib as of 7-23-14, commit hash ab98d9e78b030e1fc21b3facf3561d3ed21777e3
# In 2.4, there is iteritems(), in 3 there is just items(). *sigh*
class DBColumn(tk.Frame):
	def __init__(self, root, name):
		tk.Frame.__init__(self, root)
		self.name = name
		self.root = root
		tk.Label(self, text=name).pack()
		self.list = tk.Listbox(self, exportselection = False, yscrollcommand=root.scrollbar.set)
		self.list.bind("<MouseWheel>", root.OnMouseWheel)
		self.list.bind('<ButtonRelease-1>', self.select)
		self.list.pack()
		self.list.curselection
		self.config = self.list.config
		self.insert = self.list.insert
		# Make methods to put stuff in the list. 
		# Also, how to I access the tk.Frame methods?
	def select(self, event):
		selection = self.list.curselection()
		if selection:
			for i, j in self.root.columns.items():
				if not i == self.name:
					j.highlight(selection[0])
	def highlight(self, selection):
		self.list.selection_clear(0, self.list.size()-1)
		self.list.selection_set(selection)
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name):
		self.connection = connection
		self.columns = {}
		self.table_name = table_name
		self.column_names = [i[1] for i in self.connection.cursor().execute("pragma table_info(%s)" % self.table_name)]
		tk.Frame.__init__(self, root)
		self.scrollbar = tk.Scrollbar(self, orient = 'vertical', command = self.scroll)
		for i, j in enumerate(self.column_names):
			self.columns[j] = (DBColumn(self, j))
			self.columns[j].pack(side='left')
		self.scrollbar.pack(side='left', fill = 'y')
		self.populate()
	def scroll(self, *args):
		for i in self.columns.values():
			i.list.yview(*args)
	def OnMouseWheel(self, event):
		# Borrowed from https://stackoverflow.com/a/4068275
		for i in self.columns.values():
			i.list.yview("scroll", event.delta,"units")
		return "break"
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
	db = sqlite3.connect(db_location)
	c = db.cursor()
	root = tk.Tk()
	DB = DBList(root, db, table_name)
	DB.pack()
	root.mainloop()
	
if __name__ == "__main__":
	db = sqlite3.connect('test.db')
	c = db.cursor()
	showDB("test.db", 'test')