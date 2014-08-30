# This is here to have python 2 compatibility. Unfortunately, it doesn't work. 
# It's still here. It's not that there's an error with python 2, it just doesn't 
# do anything. Anyway, this looks fancy, but it's just imports and some function reassignments. 
try:
	import tkinter as tk
	from tkinter.filedialog import askopenfilename
	from tkinter import messagebox
except ImportError:
	import Tkinter as tk
	import tkMessageBox
	from tkFileDialog import askopenfilename
	FileNotFoundError = IOError
import sqlite3
# This isn't a regular python library, it's my own. It's for interfacing with sqlite3 tables more directly. 
import WillsLib

# This is the function called when I want to switch columns from what is in the 
# config file. 
def switchColumns(base):
	with open('showDB.config', 'r') as f:
		l = list(f)
		# Look through the config file, and whenever you find the table we're working with, remove it and it's 
		# list of columns (that's the two pop()'s in a row. 
		for i, j in enumerate(l):
			if j == sqlite3.table_name:
				l.pop(i)
				l.pop(i)
				break
	# Then rewrite the file. 
	with open("showDB.config", 'w') as f:
		for i in l:
			f.write(i)
		base.destroy()
		# This function reads the file I just rewrote, so that's all I have to do. 
		showDB(sqlite3.location, sqlite3.table_name)
		
# This is the window I bring up when you click on the add button, to add to a table. 
class addWindow(tk.Tk):
	def __init__(self, base_list):
		tk.Tk.__init__(self)
		# This is a DBList object, the list this is adding to.
		self.base_list = base_list
		# These are for the layout. Each column has a frame, in which is a 
		# label and a text box to put the new data. 
		self.frames = []
		self.boxes = []
		self.labels = []
		
		c = self.base_list.connection.cursor()
		# This gets all the columns in the list so it can put them on the screen 
		# as labels. 
		c.execute('pragma table_info(%s)' % sqlite3.table_name)
		names = [i[1] for i in c.fetchall()]
		# I set this up so that any index will correspond to the same frame, 
		# label, and text box, so it's easy to iterate through them.
		for i in names:
			# Add a new frame. 
			self.frames.append(tk.Frame(self))
			# Add a new label, with its parent the frame we just added, and 
			# the text as the name from the pragma.
			self.labels.append(tk.Label(self.frames[-1], text=str(i)+': '))
			self.labels[-1].pack(side='left')
			self.boxes.append(tk.Entry(self.frames[-1]))
			self.boxes[-1].pack(side='left')
			self.frames[-1].pack()
		tk.Button(self, text='OK', command=self.add).pack()
	def add(self):
		# This is the dictionary we're going to pass to the table itself, to be added. 
		d = {}
		for i in range(len(self.frames)):
			# The bit in brackets is just a way to get the text from the label, 
			# as that's going to be the key in the dictionary. Config() returns a
			# dictionary of all the settings a certain thing has, and so I get text,
			# which, along with the actual text, gives a bunch of other stuff, that's 
			# what the "[4]" is for. And it replaces the colon, because that's not 
			# part of the name. I should probably change it to replace a regex, so 
			# you could have a colon as part of the column name... I'll worry about
			# that later. Then we set it equal to the text from the text box. 
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
		if self.base_list.getSelected():
			if tk.messagebox.askyesno("Delete", "Are you sure you want to delete?"):
				WillsLib.DBdelete(self.base_list.connection, sqlite3.table_name, self.base_list.getSelected())
				self.base_list.populate()
class editButton(tk.Button):
	def __init__(self, root):
		tk.Button.__init__(self, root, text='Edit Selected', command=self.edit, state='disabled')
		self.root = root
		self.base_list = self.root.root
	def edit(self):
		# Only edit if there's something selected.
		if self.base_list.getSelected():
			# The index that is selected. It goes to the leftmost column, 
			# just for simplicity, and asks for its selection. 
			index = self.base_list.columns[list(self.base_list.columns.keys())[0]].list.curselection()
			window = tk.Tk()
			# See addWindow.__init__() for info on this.
			self.frames = []
			self.labels = []
			self.boxes = []
			c = self.base_list.connection.cursor()
			c.execute('pragma table_info(%s)' % sqlite3.table_name)
			for i in [i[1] for i in c.fetchall()]:
				# This is just like addWindow except for the fact that it supplies the old values in the boxes. 
				self.frames.append(tk.Frame(window))
				self.labels.append(tk.Label(self.frames[-1], text=i+': '))
				self.labels[-1].pack(side='left')
				self.boxes.append(tk.Entry(self.frames[-1]))
				# This gets the correct text straight from the actual table, 
				# that's why it's so long. It selects from the list where 
				# the last column is equal to its value at the specific index. 
				self.boxes[-1].insert('end', WillsLib.DBselect(self.base_list.connection, sqlite3.table_name, i, {list(self.base_list.columns.keys())[-1]:self.base_list.columns[list(self.base_list.columns.keys())[-1]].list.get(index)})[0])
				self.boxes[-1].pack(side='left')
				self.frames[-1].pack()
			# This is just a frame for the buttons. 
			choices = tk.Frame(window)
			ok = tk.Button(choices, text='OK', command=lambda: self.finish(index, window))
			cancel = tk.Button(choices, text='Cancel', command=window.destroy)
			ok.pack(side='left')
			cancel.pack(side='left')
			choices.pack()
	# This is just the end part of edit. 
	def finish(self, index, window):
		# This is the dictionary that's going to be added to the table. 
		set = {}
		for i, j in enumerate(self.labels):
			# See the long comment in addWindow.add() for explanation of this. 
			set[j.config()['text'][4].replace(': ', '')] = self.boxes[i].get()
		# See editButton.edit() for an explanation of the last argument in this line. 
		WillsLib.DBupdate(self.base_list.connection, sqlite3.table_name, set, {list(self.base_list.columns.keys())[-1]:self.base_list.columns[list(self.base_list.columns.keys())[-1]].list.get(index)})
		self.base_list.populate()
		window.destroy()
# This is the top row of buttons in the main window. 
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
	# This un-greys out some of the buttons when you select something. 
	def activate(self):
		for i in [self.edit, self.delete]:
			i.config(state="normal")
# This is an individual column object, from which the DBList object is made. 
class DBColumn(tk.Frame):
	def __init__(self, root, name):
		tk.Frame.__init__(self, root)
		# Name is the name of the column.
		self.name = name
		self.root = root
		# This is the actual name label above the column.
		tk.Label(self, text=name).pack()
		# This is the actual list. "exportselection = False" prevents it from 
		# losing its selection when you click on another column, and yscrollcommand
		# is for scrolling. 
		self.list = tk.Listbox(self, exportselection = False, yscrollcommand=self.scroll)
		# When you let go, this line selects the correct index across the list. 
		self.list.bind('<ButtonRelease-1>', self.select)
		self.list.pack()
		# Exposing some list methods. 
		self.config = self.list.config
		self.insert = self.list.insert
	def select(self, event):
		# The index selected. Curselection() gives a list, even though you can't
		# select more than one thing, so if you see index[0], that's why. 
		selection = self.list.curselection()
		if selection:
			# Un-grey out some buttons.
			self.root.button_box.activate()
			# For every column except me, highlight what I have highlighted. 
			for i, j in self.root.columns.items():
				if not i == self.name:
					j.highlight(selection[0])
	def highlight(self, selection):
		self.list.selection_clear(0, self.list.size()-1)
		self.list.selection_set(selection)
	# This is a method that makes scrolling with the scrollbar or arrow keys work. 
	def scroll(self, *args):
		for i in self.root.columns.values():
			if not i == self:
				i.list.yview_moveto(args[0])
		self.root.scrollbar.set(*args)
# This is the actual list object. 
class DBList(tk.Frame):
	def __init__(self, root, connection, table_name, cols):
		tk.Frame.__init__(self, root)
		# The connection to the sqlite3 table. 
		self.connection = connection
		# A dictionary of {name:column object}
		self.columns = {}
		# This is just a list of names.
		self.column_names = cols
		self.table_name = table_name
		self.switch_button = tk.Button(root, text='Switch columns', command=lambda:switchColumns(root))
		self.button_box = buttonBox(self, self.connection)
		self.button_box.pack()
		self.switch_button.pack()
		self.scrollbar = tk.Scrollbar(self, orient = 'vertical', command = self.scroll)
		# This loop actually makes the columns on the screen and puts them 
		# in the columns variable.
		for j in self.column_names:
			self.columns[j] = DBColumn(self, j)
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
	# This adds a set of values, or a row, to the list. It doesn't take 
	# care of the interface with the actual table though. Maybe I should 
	# fix that. 
	def add(self, cols):
		# Cols is a dictionary.
		if len(self.columns) != len(cols):
			raise Exception("You didn't give the right amount of columns!")
		else:
			for i, j in cols.items():
				self.columns[i].insert('end', j)
	# Clear the table and put the changed table back in. 
	def populate(self):
		rows = WillsLib.DBselect(self.connection, self.table_name, self.column_names, 'all')
		for i in self.columns.values():
			i.list.delete(0, 'end')
		for i, j in enumerate(rows):
			# This will always work because column names comes from a sqlite3 "pragma" call, 
			# and that will give the rows in the same order as a "select" call.
			self.add({self.column_names[h]:k for h, k in enumerate(j)})
	# This method gives you a dictionary of 
	# everything selected, in the format {column:selection}.
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
class BoxFrame(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root, pady=5)
		self.box = tk.Entry(self)
		self.box.pack(side='left')
		tk.Frame(self, width=22).pack(side='left')
	def get(self):
		return self.box.get()
class FirstBox(tk.Frame):
		def __init__(self, root):
			tk.Frame.__init__(self, root)
			self.root = root
			self.box = tk.Entry(self)
			img = tk.PhotoImage(master = self.root, file="icon.gif")
			self.button = tk.Button(self, image=img, command=self.root.addBox, height=15, width=15)
			self.picture = img
			self.box.pack(side='left')
			self.button.pack(side='left')
		def get(self):
			return self.box.get()
# This runs if there is no table under the given name. It asks for columns, 
# and creates a table. 
class TableCreator(tk.Tk):
	def __init__(self, connection, table_name):
		tk.Tk.__init__(self)
		self.connection = connection
		self.table_name = table_name
		tk.Label(self, text="Table name: {}".format(table_name)).pack()
		# WHATEVER YOU DECIDE ON, MAKE SURE THIS TEXT REFLECTS IT!!!!
		tk.Label(self, text="Type in the columns that will be in your \ntable, one in each box.\nPress the button for more boxes. ").pack()
		self.boxes = []
		self.boxes.append(FirstBox(self))
		for i in self.boxes:
			i.pack()
		self.done = tk.Button(self, text = "Done", command = self.create)
		self.done.pack()	
	def create(self):
		self.new_cols = [i.get().replace(' ','') for i in self.boxes]
		print(self.new_cols)
		WillsLib.DBcreate(self.connection, self.table_name, self.new_cols)
		self.destroy()
	def addBox(self):
		for i in self.boxes:
			i.pack_forget()
		self.done.pack_forget()
		self.boxes.append(BoxFrame(self))
		for i in self.boxes:
			i.pack()		
		self.done.pack()
# This is the finishing function for getCols(), which is fed from showDB(). ShowDB
# doesn't really do that much itself, it mostly just sees what the column situation
# is and gives it to getCols() if it needs to ask for columns, or to this otherwise. 
# Column_picker is the column picker window, db is the connection, and write is a boolean
# telling whether or not to write the picked columns to the config file. 
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
# This function just puts up the window that asks for the columns, and 
# then gives that information to closeCols() to finish up. 
def getCols(table_name, cursor, root, db):
	picked_columns = {}
	cursor.execute("pragma table_info(%s)" % table_name)
	tk.Label(root, text="Pick the columns you want to show").pack()
	checkboxes = []
	for i in [j[1] for j in cursor.fetchall()]:
		picked_columns[i] = tk.IntVar(root)
		checkboxes.append(tk.Checkbutton(root, text=str(i), variable=picked_columns[i]))
	for i in checkboxes:
		i.pack()
	ok_button = tk.Button(root, text="Done", command=lambda: closeCols(picked_columns, root, db, table_name, True))
	ok_button.pack()
	root.mainloop()
# This is the method you want to call if you're using this as a 
# library. This will take care of everything from start to finish. 
# You can supply the columns programmitcally with the "columns" variable, 
# it's a list, or you can leave it blank and the user can do it. 
def showDB(db_location, table_name, columns = None):
	db = sqlite3.connect(db_location)
	sqlite3.location = db_location
	sqlite3.table_name = table_name
	c = db.cursor()
	c.execute("pragma table_info({})".format(table_name))
	if(c.fetchall() == []):
		table_creator = TableCreator(db, table_name)
		table_creator.wait_window(table_creator)
	column_picker = tk.Tk()
	picked_columns = {}
	checkboxes = []
	c = db.cursor()
	if columns:
		c.execute("pragma table_info(%s)" % sqlite3.table_name)
		d = {p[1]:tk.IntVar() for p in c.fetchall()}
		for i, j in d.items():
			if i in columns:
				j.set(1)
		closeCols(d, column_picker, db, sqlite3.table_name, False)
		return
	else:
		# This is the file reading logic. If there's a file, it turns it into a 
		# list and parses it for the table and the columns that go with it, or else
		# it asks the user. 
		try:
			f = open("showDB.config", 'r')
			l = list(f)
			f.close()
		except FileNotFoundError:
			l = []
	if not l:
		# If there's nothing in the config file, ask the user.
		getCols(table_name, c, column_picker, db)
	else:
		# If there is something in the config file, go through every line... 
		for i, j in enumerate(l):
			# If it's the table name...
			if j.find(table_name) != -1:
				# Make a dict of all the columns in the table, with IntVar()'s 
				# as their values. 
				c.execute("pragma table_info(%s)" % sqlite3.table_name)
				cols = {p[1]:tk.IntVar() for p in c.fetchall()}
				for m, p in cols.items():
					try:
						# Index() throws an error if it can't find anything, so 
						# if it goes through right, than that column must be in 
						# the line, so it is set to 1, which means it's there. 
						# If it throws an error, that means it's not there, so it
						# needs to be 0. 
						l[i+1].split(',').index(m)
						p.set(1)
					except ValueError:
						p.set(0)
				closeCols(cols, column_picker, db, table_name, False)
				return
		getCols(table_name, c, column_picker, db)
class fileCreate(tk.Tk):
	def __init__(self, root):
		tk.Tk.__init__(self)
		root.destroy()
		tk.Label(self, text="Name of file, including extension (.db):").pack(side='left')
		self.box = tk.Entry(dialog)
		self.box.pack(side='left')
		tk.Button(dialog, command=self.finish).pack(side='top')
	def finish(self):
		sqlite3.location = self.box.get()
		root.destroy()
		self.destroy()
# This makes it so that, if you just run this straight, not as a library, 
# it'll ask you where the database is and show it to you. There's a bug, though, 
# when you start it, there's a file dialog, and when you close that, you're supposed
# to type the name of the table itself, but you can't actually use that box until 
# you remove focus and then bring it back. It's strange. But other than that, it works fine. 
if __name__ == "__main__":
	sqlite3.location = ''
	start = tk.Tk()
	new_file_frame = tk.Frame(start)
	tk.Button(new_file_frame, text='Create a new .db file', command=lambda: fileCreate(new_file_frame)).pack(side='left')
	tk.Button(new_file_frame, text='Find an existing .db file').pack(side='left')
	start.wait_window(start)
	start = tk.Tk()
	tk.Label(start, text='What is the name of your table?').pack()
	box = tk.Entry(start)
	box.pack()
	button = tk.Button(start, text='OK', command=lambda: showDB(location, box.get()))
	button.pack()
# 	I don't know if I need this anymore. I'll check. 
# 	start.mainloop()