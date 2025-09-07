import sqlite3

conc = sqlite3.connect('users.db')
c = conc.cursor()

c.execute('SELECT * FROM users')
print(c.fetchall())

c.execute('SELECT * FROM user_preferences')
print(c.fetchall())

conc.close()