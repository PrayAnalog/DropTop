import pymysql.cursors
import csv

# from io import open

f = open('new_staff.csv', 'r', encoding='utf-8')

# reader = csv.reader(f)
# for line in reader:
# 	linep = tuple(line)
# 	print(str(linep))



conn = pymysql.connect(host = 'localhost',
		user = 'root',
		password = 'droptop',
		db = 'BucketList',
		charset = 'utf8')

try:
	rdr = csv.reader(f)
	for line in rdr:
		linep = tuple(line)

		with conn.cursor() as cursor:
			sql = 'INSERT INTO staff VALUES'+str(linep);
			cursor.execute(sql)

		conn.commit()
 

finally: 
	conn.close()


f.close()
