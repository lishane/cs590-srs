import MySQLdb

db = MySQLdb.connect(
    host='127.0.0.1',
    user="root",
    passwd="  ",
    db="stackoverflow"
)
c = db.cursor()

c.execute("SELECT id FROM posts")
with open('questionIds.txt', 'w') as f:
    for row in c:
        f.write(str(row[0]) + '\n')
