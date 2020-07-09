import sqlite3
from sqlite3 import Error
try:
    conn = sqlite3.connect('trackdb.sqlite')
    cur = conn.cursor()

    #1. delete multiple table if exits & then create the multiple table
    cur.executescript('''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;

    CREATE TABLE "Artist"(
            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "name"	TEXT UNIQUE
    );
    CREATE TABLE "Album"(
            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "title"	TEXT UNIQUE
    );
    CREATE TABLE "Track"(
            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "len"	INTEGER,
            "rating"	INTEGER
    );
    ''')
    #2. insert single record at a time
    cur.execute('''INSERT OR IGNORE INTO Artist (name,id) VALUES ('Ashish',1)''')
    #note:here we use ignore because we use artist name is unique in table if we feed same artist name twice it will ignore it.
    #3. to read all data from a Artist table in a list
    cur.execute('SELECT * FROM Artist')
    print(cur.fetchall())

    #4.inserts many records at a time
    purchases = [(2, 1000, 5.00),
             (3, 55, 2.00),
             (4, 500, 3.00),
            ]
    cur.executemany('INSERT OR IGNORE INTO Track VALUES (?,?,?)', purchases)

    #5.print data from database by sqlquery 
    for row in cur.execute('SELECT * FROM Track ORDER BY rating'):
        print(row)

    #to read all data from a Track table in a list
    cur.execute('SELECT * FROM Track')
    print(cur.fetchall())

    #6.to update a field with where query 
    cur.execute('UPDATE Track SET len = 66 where id = 3')
    cur.execute('SELECT * FROM Track')
    print(cur.fetchall())

    #7.to count no. of rows in table
    cur.execute('SELECT COUNT(*) FROM Track')
    print(cur.fetchall())

    #8.delete a single row from the SQLite table
    cur.execute('DELETE from Track where id = 4')

    #8.1.delete a single row from the SQLite table parameterized query
    id = input('DELETE data from Track table where id = ')
    sql_update_query = """DELETE from Track where id = ?"""
    cur.execute(sql_update_query, (id, ))

    #9. delete a multiple row from the SQLite table parameterized query
    idsToDelete = [(4,),(3,)]
    sqlite_update_query1 = """DELETE from Track where id = ?"""
    cur.executemany(sqlite_update_query1, idsToDelete)

    #to read all data from a table in a list
    cur.execute('SELECT * FROM Track')
    print(cur.fetchall())
    
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
except Error as e:
    print(e)
