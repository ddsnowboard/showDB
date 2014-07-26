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
		self.list = tk.Listbox(self, exportselection = False, yscrollcommand=self.scroll)
		self.list.bind('<ButtonRelease-1>', self.select)
		self.list.pack()
		self.list.curselection
		self.config = self.list.config
		self.insert = self.list.insert
	def select(self, event):
		selection = self.list.curselection()
		if selection:
			for i, j in self.root.columns.items():
				if not i == self.name:
					j.highlight(selection[0])
	def highlight(self, selection):
		self.list.selection_clear(0, self.list.size()-1)
		self.list.selection_set(selection)
	def scroll(self, *args):
		for i in self.root.columns.values():
			if not i == self:
				i.list.yview_moveto(args[0])
		self.root.scrollbar.set(*args)
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name, cols):
		self.connection = connection
		self.columns = {}
		self.table_name = table_name
		self.column_names = cols
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
		rows = WillsLib.DBselect(self.connection, self.table_name, self.column_names, 'all')
		row_dictionary = {}
		for i, j in enumerate(rows):
			self.add({self.column_names[h]:k for h, k in enumerate(j)})
def closeCols(picked_columns, column_picker, db, table_name, write):
	if write:
		with open('showDB.config', 'a') as f:
			f.write("%s\n%s" % (table_name, ','.join([i for i, j in picked_columns.items() if j.get() == 1])))
	cols = [i for i in picked_columns.keys() if picked_columns[i].get() == 1]
	column_picker.destroy()
	if cols == []:
		return
	root = tk.Tk()
	DB = DBList(root, db, table_name, cols)
	DB.pack()
	root.mainloop()
def getCols(table_name, cursor, root):
	picked_columns = {}
	cursor.execute("pragma table_info(%s)" % table_name)
	tk.Label(root, text="Pick the columns you want to show").pack()
	checkboxes = []
	for i in cursor.fetchall():
		picked_columns[i[1]] = tk.IntVar()
		checkboxes.append(tk.Checkbutton(root, text=str(i[1]), variable=picked_columns[i[1]]))
	for i in checkboxes:
		i.pack()
	ok_button = tk.Button(root, text="Done", command=lambda: closeCols(picked_columns, root, db, table_name, True))
	ok_button.pack()
	root.mainloop()
def showDB(db_location, table_name):
	db = sqlite3.connect(db_location)
	column_picker = tk.Tk()
	picked_columns = {}
	checkboxes = []
	c = db.cursor()
	try:
		f = open("showDB.config", 'r')
		l = list(f)
		f.close()
	except FileNotFoundError:
		l = []
	if not l:
		getCols(table_name, c, column_picker)
	else:
		for i, j in enumerate(l):
			if j.find(table_name) != -1:
				cols = {p:tk.IntVar() for p in l[i+1].split(',')}
				for i in cols.values():
					i.set(1)
				closeCols(cols, column_picker, db, table_name, False)
				return
		getCols(table_name, c, column_picker)
if __name__ == "__main__":
	db = sqlite3.connect('test.db')
	c = db.cursor()
	showDB("test.db", 'test')