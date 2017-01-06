import sqlite3 as lite

db = lite.connect(r'C:\Users\abraham.cacoulides\PycharmProjects\testwebpage\test_db')
with db:
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM "prodfloor_features"''')
    all_rows=cursor.fetchall()
    for row in all_rows:
        print(row)