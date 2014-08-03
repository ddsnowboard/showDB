try:
	import tkinter as tk
	from tkinter.filedialog import askopenfilename
except ImportError:
	import Tkinter as tk
	from tkFileDialog import askopenfilename
	# dict.items = dict.iteritems
import sqlite3
import WillsLib
# In 2.4, there is iteritems(), in 3 there is just items(). *sigh*
def switchColumns(base):
	with open('showDB.config', 'r') as f:
		l = list(f)
		for i, j in enumerate(l):
			if j == sqlite3.table_name:
				l.pop(i)
				l.pop(i)
				break
	with open("showDB.config", 'w') as f:
		for i in l:
			f.write(i)
		base.destroy()
		showDB(sqlite3.location, sqlite3.table_name)
class addWindow(tk.Tk):
	def __init__(self, base_list):
		tk.Tk.__init__(self)
		self.base_list = base_list
		self.frames = []
		self.boxes = []
		self.labels = []
		c = self.base_list.connection.cursor()
		c.execute('pragma table_info(%s)' % sqlite3.table_name)
		for i in sorted([i[1] for i in c.fetchall()]):
			self.frames.append(tk.Frame(self))
			self.labels.append(tk.Label(self.frames[-1], text=str(i)+': '))
			self.labels[-1].pack(side='left')
			self.boxes.append(tk.Entry(self.frames[-1]))
			self.boxes[-1].pack(side='left')
			self.frames[-1].pack()
		tk.Button(self, text='OK', command=self.add).pack()
	def add(self):
		d = {}
		for i in range(len(self.frames)):
			d[self.labels[i].config()['text'][4].replace(': ', '')] = self.boxes[i].get()
		WillsLib.DBinsert(self.base_list.connection, sqlite3.table_name, d)
		self.base_list.populate()
		self.destroy()
class addButton(tk.Button):
	def __init__(self, root):
		tk.Button.__init__(self, root, text='Add', command=self.add)
		self.root = root
	def add(self):
		addWindow(self.root.root)
class deleteButton(tk.Button):
	def __init__(self, root):
		tk.Button.__init__(self, root, text='Delete Selected', state='disabled', command=self.delete)
		self.root = root
		self.base_list = self.root.root
	def delete(self):
		# Add a dialog box asking if you really want to delete?
		if self.base_list.getSelected():
			WillsLib.DBdelete(self.base_list.connection, sqlite3.table_name, self.base_list.getSelected())
			self.base_list.populate()
class editButton(tk.Button):
	def __init__(self, root):
		tk.Button.__init__(self, root, text='Edit Selected', command=self.edit, state='disabled')
		self.root = root
		self.base_list = self.root.root
	def edit(self):
		if self.base_list.getSelected():
			index = self.base_list.columns[list(self.base_list.columns.keys())[0]].list.curselection()
			window = tk.Tk()
			self.frames = []
			self.labels = []
			self.boxes = []
			c = self.base_list.connection.cursor()
			c.execute('pragma table_info(%s)' % sqlite3.table_name)
			for i in sorted([i[1] for i in c.fetchall()]):
				self.frames.append(tk.Frame(window))
				self.labels.append(tk.Label(self.frames[-1], text=i+': '))
				self.labels[-1].pack(side='left')
				self.boxes.append(tk.Entry(self.frames[-1]))
				self.boxes[-1].insert('end', WillsLib.DBselect(self.base_list.connection, sqlite3.table_name, i, {list(self.base_list.columns.keys())[-1]:self.base_list.columns[list(self.base_list.columns.keys())[-1]].list.get(index)})[0])
				self.boxes[-1].pack(side='left')
				self.frames[-1].pack()
			choices = tk.Frame(window)
			ok = tk.Button(choices, text='OK', command=lambda: self.finish(index, window))
			cancel = tk.Button(choices, text='Cancel', command=window.destroy)
			ok.pack(side='left')
			cancel.pack(side='left')
			choices.pack()
	def finish(self, index, window):
		set = {}
		for i, j in enumerate(self.labels):
			set[j.config()['text'][4].replace(': ', '')] = self.boxes[i].get()
		WillsLib.DBupdate(self.base_list.connection, sqlite3.table_name, set, {list(self.base_list.columns.keys())[-1]:self.base_list.columns[list(self.base_list.columns.keys())[-1]].list.get(index)})
		self.base_list.populate()
		window.destroy()
class buttonBox(tk.Frame):
	def __init__(self, root, connection):
		tk.Frame.__init__(self, root)
		self.root = root
		self.add = addButton(self)
		self.edit = editButton(self)
		self.delete = deleteButton(self)
		self.add.pack(side='left')
		self.delete.pack(side='left')
		self.edit.pack(side='left')
	def activate(self):
		for i in [self.edit, self.delete]:
			i.config(state="normal")		
class DBColumn(tk.Frame):
	def __init__(self, root, name):
		tk.Frame.__init__(self, root)
		self.name = name
		self.root = root
		tk.Label(self, text=name).pack()
		self.list = tk.Listbox(self, exportselection = False, yscrollcommand=self.scroll)
		self.list.bind('<ButtonRelease-1>', self.select)
		self.list.pack()
		self.config = self.list.config
		self.insert = self.list.insert
	def select(self, event):
		selection = self.list.curselection()
		if selection:
			# This line will activate the buttons when something is clicked, but it's not done yet. 
			self.root.button_box.activate()
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
		tk.Frame.__init__(self, root)
		self.connection = connection
		self.columns = {}
		self.table_name = table_name
		self.column_names = cols
		self.switch_button = tk.Button(root, text='Switch columns', command=lambda:switchColumns(root))
		self.button_box = buttonBox(self, self.connection)
		self.button_box.pack()
		self.switch_button.pack()
		self.scrollbar = tk.Scrollbar(self, orient = 'vertical', command = self.scroll)
		for i, j in enumerate(sorted(self.column_names)):
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
		for i in self.columns.values():
			i.list.delete(0, 'end')
		for i, j in enumerate(rows):
			self.add({self.column_names[h]:k for h, k in enumerate(j)})
	def getSelected(self):
		o = {}
		for i, j in self.columns.items():
			try:
				o[i] = j.list.get(j.list.curselection())
			except tk._tkinter.TclError:
				return None
		if o:
			return o
		else:
			return None
def closeCols(picked_columns, column_picker, db, table_name, write):
	if write:
		with open('showDB.config', 'a') as f:
			f.write("%s\n%s" % (table_name, ','.join(sorted([i for i, j in picked_columns.items() if j.get() == 1]))))
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
	sqlite3.location = db_location
	sqlite3.table_name = table_name
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
				c.execute("pragma table_info(%s)" % sqlite3.table_name)
				cols = {p[1]:tk.IntVar() for p in c.fetchall()}
				for m, p in cols.items():
					try:
						l[i+1].split(',').index(m) 
						p.set(1)
					except ValueError:
						p.set(0)
				closeCols(cols, column_picker, db, table_name, False)
				return
		getCols(table_name, c, column_picker)
if __name__ == "__main__":
	location = ''
	start = tk.Tk()
	tk.Label(text='What is the name of your table?').pack()
	box = tk.Entry(start, exportselection=0, state=tk.DISABLED)
	box.pack()
	button = tk.Button(start, text='OK', command=lambda: showDB(location, box.get()))
	button.pack()
	location = askopenfilename(defaultextension='.db', title="Choose your database", filetypes=[('Database Files', '.db'), ('All files', '*')])
	box.config(state=tk.NORMAL)
	start.mainloop()