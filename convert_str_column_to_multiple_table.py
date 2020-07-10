import pandas as pd
df = pd.read_csv('TestData.csv',encoding='ISO-8859-1')

import sqlite3
from sqlite3 import Error
'''
Note: by doing this data amount or filesize is not reduce.
It is used to scanned a particular information fastly.
It is used on "web" relational database where we have to read quickly from very large amount of data.
'''
try:
    
    #print(df.dtypes)
    #to find string type column from dataframe
    l = []
    a = df.columns
    for i in a:
        if df[i].dtype == 'object':
            print(i)
            l.append(i)
    print(l)#print the name of all string columns, here our dataset have only 3 string column
    p = l[1:]
    print(p)
    m = []
    for k in p:
        a = set(df.loc[:,k])
        e = list(a)
        #for changing string values of columns to its unique number
        dict1 = {}
        l = 0
        for i in a:
            dict1[i] = l
            l += 1
        print(dict1)
        df.loc[:,k] = [dict1[value] for value in df.loc[:,k]]
        df = df.rename(columns={k: k+"_id"})
        print(df.columns)

        #for creating a new dataframe which contain columns unique number - string data
        print(len(e))
        t = [str(i) for i in range(len(e))]
        print(e)
        print(t)
        d = pd.DataFrame(e,columns = [k])
        d.index = t
        print(d.columns)
        d.index.name = 'Id'
        print(d.index.name)
        
        print(d)
        m.append(d)
    
    print(m)
    print(len(m))#
    print(df)
    conn = sqlite3.connect('trackdb2.sqlite')
    cur = conn.cursor()

    #As here our dataset has only 3 string columns so we create only 3 table , you can create no. of table = no. of string column
    cur.executescript('''
    DROP TABLE IF EXISTS Table1;
    DROP TABLE IF EXISTS Table2;
    DROP TABLE IF EXISTS Table3;''')
    
    #create table1
    df.to_sql(name='Table1', con=conn)
    cur.execute('SELECT * FROM Table1')
    column_names = [description[0] for description in cur.description]
    print("column names:\n",column_names)
    #read table1 data
    for row in cur.execute('SELECT * FROM Table1'):
        print(row)
        
    #create table2
    m[0].to_sql(name='Table2', con=conn)
    cur.execute('SELECT * FROM Table2')
    column_names = [description[0] for description in cur.description]
    print("column names:\n",column_names)
    #read table2 data
    for row in cur.execute('SELECT * FROM Table2'):
        print(row)

    #create table3
    m[1].to_sql(name='Table3', con=conn)
    cur.execute('SELECT * FROM Table3')
    column_names = [description[0] for description in cur.description]
    print("column names:\n",column_names)
    #read table3 data
    for row in cur.execute('SELECT * FROM Table3'):
        print(row)

    #apply join operation on multiple table
    for row in cur.execute('SELECT Table1.Track_Name , Table3.Genre FROM Table1 JOIN Table3 ON Table1.Genre_id = Table3.Id'):
        print(row)
    
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
except Error as e:
    print(e)
