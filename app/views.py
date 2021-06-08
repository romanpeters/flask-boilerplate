from flask import render_template, redirect, request, make_response
import app.account as acc
from app import app, olympos
from app import database as db
from app import feed


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    print(request.form)
    sco = int(request.form['sco'])
    pwd = request.form['pwd']
    user = acc.User(sco=sco, pwd=pwd)
    if user.login_is_valid:
        print('Login successful')
        user.db.add_user_to_db()
        return redirect(f"/user/{sco}")
    print('Onbekend SCO')
    return redirect("/")

@app.route("/user/<sco>", methods=['GET'])
def account(sco):
#    available_slots = olympos.FitnessPage()
    session = db.Session()
    user = session.query(db.Users).filter_by(user_id=sco).first()
    session.close()
    print(f"It's {user.first_name}!")
    print(acc.get_account_reservations(sco))  # debug
    return render_template("user.html", reservations=acc.get_account_reservations(sco), user=user)


@app.route("/ical/<sco>", methods=['GET'])
def ical(sco):
    feed.to_ical(int(sco))
    path = f'data/{sco}.ics'
    with open(path, 'rb') as f:
        text = f.read()
    resp = make_response(text, 200)
    resp.headers.extend({'Content-type': 'text/calendar'})
    return resp