from googletrans import Translator
import pymysql



def main():
	t = Translator()

	
	table_name = "batter"
	select_sql = "SELECT name FROM " + table_name
	update_sql = "UPDATE " + table_name + " SET name = '%s'" + " WHERE name = '%s'"

	try:
		db = pymysql.connect("localhost","root","droptop","BucketList", charset="utf8")
		cursor = db.cursor()

		cursor.execute(select_sql)
		rows = cursor.fetchall()

		for row in rows:
			korean_name = row[0]
			# print(korean_name)
			english_name = t.translate(korean_name).text
			print(korean_name + " -> " + english_name)

			# cursor.execute(update_sql % (english_name, korean_name))
			# db.commit()
			# break


	except Exception as e:
		print(str(e))
		# db.rollback()

	finally:
		db.close()



main()