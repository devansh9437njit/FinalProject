from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response, request, redirect, jsonify, render_template

app = Flask(__name__)


connection = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="dev"
)
cursor = connection.cursor(dictionary=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/search', methods=["POST"])
def all():

    #where date(game_date) between date('2012-11-03') and date('2012-11-05')

    data = request.form
    start = data["start"]
    end = data["end"]
    yearly = "off"
    try:
        yearly = data["yearly"]

    except:
        pass

    query = f'SELECT * FROM dev.prices WHERE DATE(`Date`) BETWEEN DATE("{start}") AND DATE("{end}")'

    if yearly == "on":
        query += " AND MONTH(Date) = 1;"

    print(query)
    
    cursor.execute(query)

    result = cursor.fetchall()

    

    labels = result[0]
    la = []
    dates = []
    fl = []
    sf = []
    wa = []
    bo = []
    ny = []

    for i in result:
        la.append(i["CA-Los Angeles"])

    for i in result:
        dates.append(i["Date"])

    for i in result:
        fl.append(i["FL-Miami"])

    for i in result:
        sf.append(i["CA-San Francisco"])

    for i in result:
        wa.append(i["DC-Washington"])

    for i in result:
        bo.append(i["MA-Boston"])

    for i in result:
        ny.append(i["NY-New York"])

    print(dates)

    return render_template("main.html", labels=labels,
                           la=la,
                           dates=dates,
                           fl=fl,
                           sf=sf,
                           wa=wa,
                           bo=bo,
                           ny=ny)
    # return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
