import sqlite3
def sanitize(string):
	WORD_LIST = ['ABORT', 'ACTION', 'ADD', 'AFTER', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'ATTACH', 'AUTOINCREMENT', 'BEFORE', 'BEGIN', 'BETWEEN', 'BY', 'CASCADE', 'CASE', 'CAST', 'CHECK', 'COLLATE', 'COLUMN', 'COMMIT', 'CONFLICT', 'CONSTRAINT', 'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'DATABASE', 'DEFAULT', 'DEFERRABLE', 'DEFERRED', 'DELETE', 'DESC', 'DETACH', 'DISTINCT', 'DROP', 'EACH', 'ELSE', 'END', 'ESCAPE', 'EXCEPT', 'EXCLUSIVE', 'EXISTS', 'EXPLAIN', 'FAIL', 'FOR', 'FOREIGN', 'FROM', 'FULL', 'GLOB', 'GROUP', 'HAVING', 'IF', 'IGNORE', 'IMMEDIATE', 'IN', 'INDEX', 'INDEXED', 'INITIALLY', 'INNER', 'INSERT', 'INSTEAD', 'INTERSECT', 'INTO', 'IS', 'ISNULL', 'JOIN', 'KEY', 'LEFT', 'LIKE', 'LIMIT', 'MATCH', 'NATURAL', 'NO', 'NOT', 'NOTNULL', 'NULL', 'OF', 'OFFSET', 'ON', 'OR', 'ORDER', 'OUTER', 'PLAN', 'PRAGMA', 'PRIMARY', 'QUERY', 'RAISE', 'RECURSIVE', 'REFERENCES', 'REGEXP', 'REINDEX', 'RELEASE', 'RENAME', 'REPLACE', 'RESTRICT', 'RIGHT', 'ROLLBACK', 'ROW', 'SAVEPOINT', 'SELECT', 'SET', 'TABLE', 'TEMP', 'TEMPORARY', 'THEN', 'TO', 'TRANSACTION', 'TRIGGER', 'UNION', 'UNIQUE', 'UPDATE', 'USING', 'VACUUM', 'VALUES', 'VIEW', 'VIRTUAL', 'WHEN', 'WHERE', 'WITH', 'WITHOUT']
	for i in WORD_LIST:
		if ' '+i.lower()+' ' in string.lower() or ', '+i.lower() in string.lower() or string.lower() == i.lower():
			if i == 'DROP':
				raise Exception("You should not have used \"Drop\" in your input. Please use a different word")
			else:
				string = string.lower().replace(i.lower(),"'"+i.lower()+"'")
	return string
def DBinsert(connection, table_name, vals):
	if type(vals) == type([]):
		s = 'insert into '+sanitize(table_name)+' VALUES (?'
		for i in range(len(vals)-1):
			s += ",?"
		s+=');'
		connection.cursor().execute(s, tuple(vals))
	elif type(vals) == type({}):
		s = 'insert into %s(' % sanitize(table_name)
		s += ','.join([sanitize(i) for i in vals.keys()])
		s+=') VALUES (?'
		for i in range(len(vals.values())-1):
			s +=',?'
		s += ');'
		connection.cursor().execute(s, tuple(vals.values()))
	connection.commit()
def DBselect(connection, table_name, columns, which):
	out = []
	if columns == 'all':
		columns = ['*']
	elif type(columns) == str:
		columns = [columns]
	else:
		for i, j in enumerate(columns):
			columns[i] = sanitize(str(j))
	if which == 'all':
		for i in connection.cursor().execute('select %s from %s;' % (','.join(columns),sanitize(table_name))):
			out.append(i)
	else:
		strings = [sanitize(i) + " = ?" for i in which.keys()]
		for i in connection.cursor().execute("select %s from %s WHERE %s" % (','.join(columns), sanitize(table_name), ' and '.join(strings)), tuple([i for i in which.values()])):
			out.append(i)
	return out
def DBcreate(connection, table_name, columns):
	s = 'create table '+sanitize(table_name)+'('
	s+= ', '.join([sanitize(i) for i in columns])
	s+=');'
	print(s)
	connection.cursor().execute(s)
	connection.commit()
def DBupdate(connection, table_name, set, which):
	# Set and which will be dictionaries that have the syntax {column: value}
	# "Which" could also be the string "all"
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
	for i in set.keys():
		strings.append(sanitize(str(i))+' = ?')
	if which == 'all':
		connection.cursor().execute("update "+sanitize(table_name)+" SET "+', '.join(strings),tuple([j for j in set.values()]))
		connection.commit()
	else:
		params = []
		for i in which.keys():
			params.append(sanitize(str(i))+' = ?')
		connection.cursor().execute("update "+table_name+" SET "+', '.join(strings)+" WHERE "+' and '.join(params),tuple([j for j in set.values()]+[i for i in which.values()]))
	connection.commit()
def DBdelete(connection, table_name, which):
	if which == 'all':
		connection.cursor().execute("delete from %s" % sanitize(table_name))
		db.commit()
		return
	strings = [sanitize(i)+ " = ?" for i in which.keys()]
	connection.cursor().execute("delete from "+sanitize(table_name)+" WHERE "+' and '.join(strings),tuple([i for i in which.values()]))
	connection.commit()