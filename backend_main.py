import datetime
import math
import random
import time
from multiprocessing import Process

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
import bcrypt

import sys
sys.path.append("/root/uefa")

from hetzner.mails_reg import creator_emails, create_driver
from uefa.uefa_site_reg.site_reg_func import start_registration
from hetzner.mails_reg.emails_message_exchange import message_exchange

app = Flask(__name__)
app.secret_key = 'mgJ5CVLv@dyfOJOg-opo5qKJ$-v2Wr'

app.config['MYSQL_HOST'] = 'e98673fl.beget.tech'
app.config['MYSQL_USER'] = 'e98673fl_uefa'
app.config['MYSQL_PASSWORD'] = 'EzDNp&Q7CK*9wQnP'
app.config['MYSQL_DB'] = 'e98673fl_uefa'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Список Proxy адресов
proxy_list = [["188.130.184.242", "1050"],
              ["45.86.1.58", "1050"]
              ]


def start_hetzner(count, hetzner_acc, hetzner_password, country, champ_club, europe_club, male_club, female_club):
    proxy_ip, proxy_port = random.choice(proxy_list)
    driver = create_driver.create_driver(proxy_ip, proxy_port)
    creator_emails.creator_emails(driver, count, hetzner_acc, hetzner_password,
                                  country, champ_club, europe_club, male_club, female_club)


def start_uefa_reg(accounts, link):
    start_registration(accounts, link)


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        user = User(user_data['id'], user_data['username'])
        return user
    return None


@app.route('/index')
@app.route('/')
@login_required
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `hetzner_manage`")
    hetzner_accounts = cur.fetchall()
    cur.execute("SELECT name FROM `clubs` WHERE club_type = 'europe_league'")
    europe_league_clubs = cur.fetchall()
    cur.execute("SELECT name FROM `clubs` WHERE club_type = 'champions_league'")
    champions_league_clubs = cur.fetchall()
    cur.execute("SELECT value FROM `countries`")
    countries = cur.fetchall()
    cur.close()
    return render_template('hetzner_mail_creation.html',
                           hetzner_accounts=hetzner_accounts,
                           europe_league_clubs=europe_league_clubs,
                           champions_league_clubs=champions_league_clubs,
                           countries=countries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", (username,))

        if result > 0:
            user_data = cur.fetchone()
            cur.close()
            password_hash = user_data['password']

            if bcrypt.checkpw(password_candidate.encode('utf-8'), password_hash.encode('utf-8')):
                user = User(user_data['id'], user_data['username'])
                login_user(user)
                return redirect(url_for('index'))
            else:
                error = 'Неверный пароль'
                return render_template('login.html', error=error)
        else:
            cur.close()
            error = 'Пользователь не найден'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/hetzner_mail_creation',  methods=["POST"])
def hetzner_mail_creation():
    hetzner_acc = request.form.get("hetzner_acc")
    country, champ_club, europe_club, male_club, female_club = request.form.get("country-input"),\
                                                               request.form.get("champ_club-input"), \
                                                               request.form.get("europe_club-input"),\
                                                               request.form.get("male_club-input"),\
                                                               request.form.get("female_club-input")

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `hetzner_manage` WHERE email = '{hetzner_acc}'")
    hetzner_acc = cur.fetchone()
    cur.close()
    count = request.form.get("hetzner-count")
    count = int(count)
    processes = request.form.get("hetzner-processes-count")
    processes = int(processes)
    per_process = math.ceil(count / processes)
    for i in range(processes):
        if count - per_process < 0:
            process = Process(target=start_hetzner, args=(count, hetzner_acc["email"], hetzner_acc["password"],
                                                          country, champ_club, europe_club, male_club, female_club))
            process.start()
        else:
            process = Process(target=start_hetzner, args=(per_process, hetzner_acc["email"], hetzner_acc["password"],
                                                          country, champ_club, europe_club, male_club, female_club))
            process.start()
        count -= per_process
    return redirect(url_for('index'))


@app.route('/mail_for_uefa')
def mail_for_uefa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `uefa_base_accounts` WHERE is_on_uefa = 0;")
    user_data = cur.fetchall()
    cur.close()
    return render_template("mail_for_uefa.html", accounts=user_data)


@app.route('/create_uefa_accounts', methods=["POST"])
def create_uefa_accounts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `uefa_base_accounts` WHERE is_on_uefa = 0;")
    user_data = cur.fetchall()
    cur.close()
    count = request.form.get("uefa-processes-count")
    count = int(count)

    accounts = [user_data[i:i+math.ceil(len(user_data) / count)] for i in range(0, len(user_data),
                                                                                math.ceil(len(user_data) / count))]
    for idx in range(count):
        process = Process(target=start_uefa_reg, args=(accounts[idx], "https://www.uefa.com/"))
        process.start()
    return redirect(url_for('mail_for_uefa'))


@app.route('/mail_list')
def mail_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `uefa_base_accounts`")
    user_data = cur.fetchall()[::-1]
    cur.close()
    return render_template("all_mails.html", accounts=user_data)


@app.route('/hetzner_for_management_creation', methods=["POST"])
def hetzner_for_management_creation():
    mail, password = request.form.get("hetzner-manage-email"), request.form.get("hetzner-manage-password")
    cur = mysql.connection.cursor()

    cur.execute(f"INSERT INTO `hetzner_manage` (email, password) VALUES ('{mail}', '{password}');")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


@app.route('/message_exchange', methods=["POST", "GET"])
def message_exchange_bk():
    if request.method == "GET":
        date = datetime.datetime.date(datetime.datetime.now())
        return render_template("message_exchange.html", date=date)
    elif request.method == "POST":
        need_date = request.form.get("message-exchange-input")
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `uefa_base_accounts` WHERE last_message_date >= '{need_date}'"
                    f" OR last_message_date IS NULL")
        accounts_to_exchange = cur.fetchall()
        cur.execute(f"SELECT mail FROM `uefa_base_accounts`")
        random_mails_list = cur.fetchall()
        random_mails_list = [i["mail"] for i in random_mails_list]
        cur.close()
        accounts_to_messaging = []
        for acc in accounts_to_exchange:
            sender_email, sender_password, recipient_email = acc["mail"], acc["password"],\
                                                             random.choice(random_mails_list)
            accounts_to_messaging.append([sender_email, sender_password, recipient_email])

        process = Process(target=message_exchange, args=(accounts_to_messaging,))
        process.start()

        date = datetime.datetime.date(datetime.datetime.now())
        return render_template("message_exchange.html", date=date)


@app.route('/mail_for_tournament')
def mail_for_tournament():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `example_tournament_accounts`")
    user_data = cur.fetchall()
    cur.close()
    return render_template("mail_for_tournament.html", accounts=user_data)


if __name__ == '__main__':
    app.run(debug=True, host="185.192.246.177", port="5000")
