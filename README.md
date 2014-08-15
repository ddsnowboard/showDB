showDB
======


#Important:
You must have WillsLib in the same directory whence you're running showDB or else it won't work. 


Shows a sqlite3 database visually. It can also do some rather rudementary editing. You can pick any database you want and any columns you want from that database, and you can switch whenever, but it will remember the columns between occasions. You can run it as a standalone program, or use it as a module with just one method, which I'll talk about right now.


######showDB(location, DB_name)

Give the file location of the database and it's name, and it'll show it in a tkinter GUI. Pretty simple. Might add option to programmatically pick columns soon, but for now there's a GUI for that too. 
