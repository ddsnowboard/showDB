import sqlite3
import tkinter as tk
# Put main DB interface functions from tshirtPicker in here. Generalize them, and they'll be useful. 
# Instead of this 'if params' business, just have a DBget() to get a specific 
# one and a DBselect to get all of them. 
# Also, it would be cool to have a table object that is really python-y instead of
# all annoying and sql-y. 
def DBinsert(connection, table_name, vals):
	s = 'insert into '+table_name+' VALUES (?'
	for i in range(len(vals)-1):
		s+=",?"
	s+=');'
	connection.cursor().execute(s, tuple(vals))
	connection.commit()
def DBselect(connection, table_name, columns):
	out = []
	if columns == 'all':
		columns = ['*']
	elif columns is list:
		for i, j in enumerate(columns):
			columns[i] = str(j)
	else:
		columns = [str(columns)]
	for i in connection.cursor().execute('select '+', '.join(columns) +' from '+table_name):
		out.append(i)
	return out
def DBcreate(connection, table_name, columns):
	s = 'create table '+table_name+'('
	for i in columns:
		s+=i
	s+=');'
	connection.cursor().execute(s)