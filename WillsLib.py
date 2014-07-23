import sqlite3
import tkinter as tk
# Put main DB interface functions from tshirtPicker in here. Generalize them, and they'll be useful. 
# Instead of this 'if params' business, just have a DBget() to get a specific 
# one and a DBselect to get all of them. 
# Also, it would be cool to have a table object that is really pythonic instead of
# all annoying and sql-y. 
def DBinsert(connection, table_name, vals):
	s = 'insert into '+table_name+' VALUES (?'
	for i in range(len(vals)-1):
		s+=",?"
	s+=');'
	connection.cursor().execute(s, tuple(vals))
	connection.commit()
def DBselect(connection, table_name, columns, which):
	out = []
	if columns == 'all':
		columns = ['*']
	elif columns is list:
		for i, j in enumerate(columns):
			columns[i] = str(j)
	else:
		columns = [str(columns)]
	if which == 'all':
		for i in connection.cursor().execute('select '+', '.join(columns) +' from '+table_name):
			out.append(i)
	else:
		strings = [i + " = ?" for i in sorted(which.keys())]
		for i in connection.cursor().execute("select %s from %s WHERE %s" % (', '.join(columns), table_name, ' and '.join(strings)), tuple([i for i in sorted(which.values())])):
			out.append(i)
	return out
def DBcreate(connection, table_name, columns):
	s = 'create table '+table_name+'('
	for i in columns:
		s+=i
	s+=');'
	connection.cursor().execute(s)
	connection.commit()
def DBupdate(connection, table_name, set, which):
	# Set and which will be dictionaries that have the syntax {column: value}\\
	# Which could also be the string "all"
	if not set:
		raise Exception("""You didn't give the right parameters!\nYou need 
						 to give 2 dictionaries, \"set\" and \"which\", that\n
						 are in the format {attribute:value}. See the \n
						 documentation for more details.""")
	elif not which:
		raise Exception("""You didn't give the right parameters!\nYou need 
						 to give 2 dictionaries, \"set\" and \"which\", that\n
						 are in the format {attribute:value}. See the \n
						 documentation for more details.\n
						 If you want to select all and change, use\n
						 which='all'""")
	strings = []
	for i in sorted(set.keys()):
		strings.append(str(i)+' = ?')
	if which == 'all':
		connection.cursor().execute("update "+table_name+" SET "+', '.join(strings),tuple([j for j in sorted(set.values())]))
		connection.commit()
	else:
		params = []
		for i in sorted(which.keys()):
			params.append(str(i)+' = ?')
		connection.cursor().execute("update "+table_name+" SET "+', '.join(strings)+" WHERE "+' and '.join(params),tuple([j for j in sorted(set.values())]+[i for i in sorted(which.values())]))
	connection.commit()
def DBdelete(connection, table_name, which):
	if which == 'all':
		connection.cursor().execute("delete from %s" % table_name)
		db.commit()
		return
	strings = [i + " = ?" for i in sorted(which.keys())]
	connection.cursor().execute("delete from "+table_name+" WHERE "+' and '.join(strings),tuple([i for i in sorted(which.values())]))
	connection.commit()