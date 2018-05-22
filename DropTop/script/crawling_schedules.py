import requests
import json

import pymysql

from bs4 import BeautifulSoup

def main():
	url = "https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList"

	payload = "leId=1&gameMonth=07&seasonId=2018&srIdList=0%2C9&teamId="
	headers = {
	    'Host': "www.koreabaseball.com",
	    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0",
	    'Accept': "application/json, text/javascript, */*; q=0.01",
	    'Accept-Language': "en-US,en;q=0.5",
	    'Accept-Encoding': "gzip, deflate, br",
	    'Referer': "https://www.koreabaseball.com/Schedule/Schedule.aspx",
	    'Content-Type': "application/x-www-form-urlencoded",
	    'X-Requested-With': "XMLHttpRequest",
	    'Content-Length': "56",
	    'Cookie': "ASP.NET_SessionId=tkb5vgwxawsjh50vzg1ibkky",
	    'Connection': "keep-alive",
	    'Cache-Control': "no-cache",
	    'Postman-Token': "65f05e80-0e88-4d4f-9140-4fa4f5156399"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	response_json = json.loads(response.text)

	# response_json_file = open("2018_5.json", "w")
	# json.dump(response_json, response_json_file, indent = 2)
	# response_json_file.close()

	team_dict = {'두산':1, 'SK':2, '한화':3, 'KIA':4, '롯데':5, 'LG':6, '넥센':7, 'KT':8, '삼성':9, 'NC':10}

	db = pymysql.connect("localhost","root","droptop","BucketList")
	cursor = db.cursor()
	sql_with_score = "INSERT INTO schedules_of_games(DATE, HOME_TEAM_ID, HOME_TEAM_SCORE, AWAY_TEAM_ID, AWAY_TEAM_SCORE) VALUES ('%s', '%d', '%d', '%d', '%d')"
	sql_with_no_score = "INSERT INTO schedules_of_games(DATE, HOME_TEAM_ID, HOME_TEAM_SCORE, AWAY_TEAM_ID, AWAY_TEAM_SCORE) VALUES ('%s', '%d', NULL, '%d', NULL)"
	# values = ('2018.05.12', 1, 2)
	# try:
	# 	cursor.execute(sql_with_no_score % values)
	# 	db.commit()
	# except Exception as e:
	# 	print(str(e))
	# 	db.rollback()

	

	for rows in response_json['rows']:
		for row in rows['row']:
			if row['Class'] == 'day':
				day = "2018." + row['Text'].split("(")[0]
				print(day)
			if row['Class'] == 'play':
				text = row['Text']
				soup = BeautifulSoup(text, 'html.parser')
				span = soup.find_all('span')
				# print(len(span))
				if len(span) == 3:	# no game result
					home_team = span[0].contents[0]
					home_team_score = None
					away_team = span[2].contents[0]
					away_team_score = None
					cursor.execute(sql_with_no_score % (day, team_dict[home_team], team_dict[away_team]))
					# print(str(home_team) + "vs" + str(away_team))
				elif len(span) == 5:
					home_team = span[0].contents[0]
					home_team_score = span[1].contents[0]
					away_team = span[4].contents[0]
					away_team_score = span[3].contents[0]
					cursor.execute(sql_with_score % (day, team_dict[home_team], int(home_team_score), team_dict[away_team], int(away_team_score)))
					# print(str(home_team) + " "  + str(home_team_score) + " vs " + str(away_team_score) + " " + str(away_team))

	db.commit()
	db.close()


	# print(response.text)

	# print(page)

	# soup = BeautifulSoup(page.text, 'html.parser')
	# artist_name_list = soup.find('tbody')
	# print(artist_name_list)
	# artist_name_list_items = artist_name_list.find_all('tr')

	# for artist_name in artist_name_list_items:
		# print(artist_name.prettify())

	# print("hello world!")

main()