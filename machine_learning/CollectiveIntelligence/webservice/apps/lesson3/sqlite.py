#!/usr/bin/env python
#_*_ encoding=utf-8 _*_
import sqlite3

def hello_world():
    ''' sqlite hello world
    '''
    conn = sqlite3.connect('/tmp/example')

    c = conn.cursor()

    # Create table
    c.execute('''create table stocks
    (date text, trans text, symbol text,
     qty real, price real)''')

    # Insert a row of data
    c.execute("""insert into stocks
              values ('2006-01-05','BUY','RHAT',100,35.14)""")

    # Save (commit) the changes
    conn.commit()

    c.execute('select * from stocks')

    # We can also close the cursor if we are done with it
    c.close()

if __name__ == '__main__':
    hello_world()

