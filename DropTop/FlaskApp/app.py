from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "droptop"
app.config["MYSQL_DATABASE_DB"] = "BucketList"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)


@app.route("/")
@app.route("/main")
def main():
	return render_template("index.html")

@app.route("/showSignUp")
def showSignUp():
	return render_template("signup.html")

@app.route("/signUp", methods=["POST"])
def signUp():
	try:
		_name = request.form["inputName"]
		_email = request.form["inputEmail"]
		_password = request.form["inputPassword"]

		# validate the received values
		if _name and _email and _password:
			# All Good, let"s call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(_password)
			cursor.callproc("sp_createUser",(_name,_email,_hashed_password))
			data = cursor.fetchall()


			if len(data) is 0:
				conn.commit()
				# return redirect("/showSignIn")
				return json.dumps({"message":"User created successfully !"})
			else:
				return json.dumps({"error":str(data[0])})

		else:
			return json.dumps({"html":"<span>Enter the required fields</span>"})

	except Exception as e:
		return json.dumps({"error":str(e)})

	finally:
		cursor.close() 
		conn.close()

@app.route("/showSingIn")
def showSignIn():
	return render_template("signin.html")


@app.route("/validateLogin", methods=["POST"])
def validateLogin():
	try:
		_username = request.form["inputEmail"]
		_password = request.form["inputPassword"]

		if _username and _password:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc("sp_validateLogin", (_username))

			data = cursor.fetchall()

			if len(data) > 0:
				if check_password_hash(str(data[0][3]), _password):
					return redirect("/userhome")
				else:
					return render_template('error.html',error = 'Wrong Email address or Password.')

			else:
				return render_template('error.html',error = 'Wrong Email address or Password.')

	except Exception as e:
		return render_template("error.html", error=str(e))


@app.route("/userhome")
def userhome():
	return render_template("/userhome.html")

@app.route("/showteam")
def showteam():
	return render_template("/showteam.html")


@app.route("/getTeam")
def getTeam():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc("sp_getTeam")

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

			}
			teams_dict.append(team_dict)

		return json.dumps(teams_dict)

	except Exception as e:
		return render_template("error.html", error=str(e))


@app.route("/showschedules")
def showschedules():
	return render_template("/showschedules.html")

@app.route("/getSchedules")
def getSchedules():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc("sp_getSchedules")

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

	except Exception as e:
		return render_template("error.html", error=str(e))


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
		

