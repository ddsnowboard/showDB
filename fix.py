# This is a bug reproduction. When you run it, it gives you a file picker,
# and when you close it, you can't use the textbox until you focus on another
# window and then focus back. This is just around so I can have something to 
# paste on websites to get help.

import tkinter as tk
from tkinter.filedialog import askopenfilename
location = ''
start = tk.Tk()
tk.Label(text='What is the name of your table?').pack()
box = tk.Entry(start, exportselection=0, state=tk.DISABLED)
box.pack()
button = tk.Button(start, text='OK', command=lambda e: None)
button.pack()
location = askopenfilename(defaultextension='.db', title="Choose your database", filetypes=[('Database Files', '.db'), ('All files', '*')])
box.config(state=tk.NORMAL)
start.mainloop()