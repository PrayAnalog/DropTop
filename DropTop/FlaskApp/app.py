from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "droptop"
app.config["MYSQL_DATABASE_DB"] = "BucketList"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)

@app.route("/")
@app.route("/Home_1")
def Home():
  return render_template('Home_1.html')

@app.route("/getBatterRank")
def getBatterRank():

  try:
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('sp_getTopBrank')

    branks= cursor.fetchall()
    branks_dict = []
    for brank in branks:
      brank_dict = {
        'team':brank[0],
        'name':brank[1],
        'avg':brank[2]
      }
      branks_dict.append(brank_dict)
    return json.dumps(branks_dict)

  except Exception as e:
    return render_template('error.html', error = str(e))

@app.route("/getPitcherRank")
def getPitcherRank():
  try:
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('sp_getTopPrank')

    pranks = cursor.fetchall()
    pranks_dict = []
    for prank in pranks:
      prank_dict = {
        'team': prank[0],
        'name': prank[1],
        'w':prank[2]
        }
      pranks_dict.append(prank_dict)
    return json.dumps(pranks_dict)

  except Exception as e:
    return render_template('error.html', error = str(e))
    
@app.route("/getTSchedules")
def getTSchedules():
  try:
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('sp_getTSchedules')

    schedules = cursor.fetchall()
    schedules_dict = []
    for schedule in schedules:
      schedule_dict = {
        'date': schedule[1],
        'home_team': schedule[2],
        'away_team':schedule[4]
        }
      schedules_dict.append(schedule_dict)
    return json.dumps(schedules_dict)

  except Exception as e:
    return render_template('error.html', error = str(e))



@app.route("/showteam")
def showteam():
	team_id = request.args.get('team_id', default = 1, type = int)
	return render_template("/showteam.html", team_id = team_id)


@app.route("/getSchedules")
def getSchedules():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		date = datetime.datetime.now()
		cursor.callproc("sp_getSchedules", (team_id, date))

		schedules = cursor.fetchall()

		schedules_dict = []

		for schedule in schedules:
			if schedule[3] == None:
				schedule_dict = {
					"date" :schedule[1],
					"home_team_name": schedule[2],
					"home_team_score": "-",
					"away_team_name": schedule[4],
					"away_team_score": "-",
				}
			else:
				schedule_dict = {
					"date" :schedule[1],
					"home_team_name": schedule[2],
					"home_team_score": schedule[3],
					"away_team_name": schedule[4],
					"away_team_score": schedule[5],
				}
			schedules_dict.append(schedule_dict)

		return json.dumps(schedules_dict)

		return json.dumps(teams_dict)

	except Exception as e:
		return render_template("error.html", error=str(e))



@app.route("/getTeam")
def getTeam():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getTeam", (team_id,))

		teams = cursor.fetchall()

		teams_dict = []

		for team in teams:
			team_dict = {
				"team_name" :team[1],
				"total_game_count" :team[2],
				"winning_count" :team[3],
				"drawing_count" :team[4],
				"losing_count" :team[5],
				"winning_rate" :team[6],
				"games_behind" :team[7],
				"consecutive_winning_count" :team[8],
				"stadium" :team[9],
				"img" :team[10],
				"youtube" : team[11]

			}
			teams_dict.append(team_dict)

		return json.dumps(teams_dict)

	except Exception as e:
		# return json.dump([])
		return render_template("error.html", error=str(e))


@app.route("/showstaff")
def showstaff():
	team_id = request.args.get('team_id', default = 1, type = int)
	return render_template("/showstaff.html", team_id = team_id)


@app.route("/getstaffs")
def getstaffs():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getStaff", (team_id,))

		staffs = cursor.fetchall()

		staffs_dict = []

		for staff in staffs:
			staff_dict = {
        # 'team': staff[0],
        'name': staff[2],
        'num': staff[3],
        'year': staff[4],
        'job': staff[5]

			}
			staffs_dict.append(staff_dict)

		return json.dumps(staffs_dict)

	except Exception as e:
		return render_template("error.html", error=str(e))


@app.route("/showbatter")
def showbatter():
	team_id = request.args.get('team_id', default = 1, type = int)
	return render_template("/showbatter.html", team_id = team_id)


@app.route("/getbatters")
def getbatters():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getBatter", (team_id,))

		batters = cursor.fetchall()

		batters_dict = []

		for batter in batters:
			batter_dict = {
        'name': batter[1],
        # 'team': batter[1],
        'avg': batter[3],
        'g': batter[4],
        'pa': batter[5],
        'ab': batter[6],
        'r': batter[7],
        'h': batter[8],
        'twob': batter[9],
        'threeb': batter[10],
        'hr': batter[11],
        'tb': batter[12],
        'rbi': batter[13],
        'sac': batter[14],
        'sf': batter[15]

			}
			batters_dict.append(batter_dict)

		return json.dumps(batters_dict)

	except Exception as e:
		return render_template("error.html", error=str(e))


@app.route("/showpitcher")
def showpichter():
	team_id = request.args.get('team_id', default = 1, type = int)
	return render_template("/showpitcher.html", team_id = team_id)

@app.route("/getpitchers")
def getpitchers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getPitcher", (team_id,))
		pitchers = cursor.fetchall()
		pitchers_dict=[]


		for pitcher in pitchers:
			pitcher_dict = {
				'name': pitcher[1],
				# 'team': pitcher[1],
				'era': pitcher[3],
				'g': pitcher[4],
				'w': pitcher[5],
				'l': pitcher[6],
				'sv': pitcher[7],
				'hid': pitcher[8],
				'wpct': pitcher[9],
				'ip': pitcher[10],
				'h': pitcher[11],
				'hr': pitcher[12],
				'bb': pitcher[13],
				'hbp':pitcher[14],
				'so': pitcher[15],
				'r': pitcher[16],
				'er': pitcher[17],
				'whip': pitcher[18]
			}
			pitchers_dict.append(pitcher_dict)

		return json.dumps(pitchers_dict)

	except Exception as e:
		return render_template("error.html", error=str(e))



@app.route("/getBattingAVG")
def getBattingAVG():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getBattingAVG", (team_id,))
		avg = cursor.fetchall()


		return json.dumps([{'battingAVG' : avg[0]}])

	except Exception as e:
		return render_template("error.html", error=str(e))


@app.route("/showballpark")
def showballpark():
	team_id = request.args.get('team_id', default = 1, type = int)
	return render_template("/showballpark.html", team_id = team_id)


@app.route("/getballpark")
def getballpark():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		team_id = request.args.get('team_id', default = 1, type = int)
		cursor.callproc("sp_getBallpark", (team_id,))
		ballparks = cursor.fetchall()

		ballparks_dict=[]


		for ballpark in ballparks:
			ballpark_dict = {
				'name': ballpark[0],
				'location': ballpark[1],
				'left': ballpark[2],
				'middle': ballpark[3],
				'right': ballpark[4],
				'fence': ballpark[5],
				'affordance': ballpark[6],
				'img': ballpark[7]
			}
			ballparks_dict.append(ballpark_dict)

		return json.dumps(ballparks_dict)

	except Exception as e:
		return render_template('error.html', error=str(e))


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
		

