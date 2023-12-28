import datetime

import pymysql

# database_con = pymysql.connect(
#     host="e98673fl.beget.tech",
#     port=3306,
#     user="e98673fl_uefa",
#     password="EzDNp&Q7CK*9wQnP",
#     database="e98673fl_uefa",
# )


def create_database_local_connection():

    database_connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="lapa2174945",
        database="testdb",
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = database_connection.cursor()

    return database_connection, cursor


def create_database_connection():

    database_connection = pymysql.connect(
        host="e98673fl.beget.tech",
        port=3306,
        user="e98673fl_uefa",
        password="EzDNp&Q7CK*9wQnP",
        database="e98673fl_uefa",
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = database_connection.cursor()

    return database_connection, cursor


def create_base_accounts_table():
    database_con, cursor = create_database_connection()

    create_base_accounts_table_query = "CREATE TABLE `uefa_base_accounts` (" \
                                       "id int AUTO_INCREMENT," \
                                       "mail varchar(128)," \
                                       "password varchar(128)," \
                                       "is_on_uefa int DEFAULT 0," \
                                       "last_message_date date," \
                                       "last_addressee varchar(128)," \
                                       "message_text text," \
                                       "country varchar(256)," \
                                       "champ_club varchar(256)," \
                                       "europe_club varchar(256)," \
                                       "male_club varchar(256)," \
                                       "female_club varchar(256)," \
                                       "is_active int DEFAULT 1," \
                                       "PRIMARY KEY (id)," \
                                       "UNIQUE (mail))"
    cursor.execute(create_base_accounts_table_query)
    cursor.close(),
    database_con.close()


def create_new_tournament_accounts_table(tournament_name="example_tournament"):
    database_con, cursor = create_database_connection()

    create_tournament_accounts_table_query = f"CREATE TABLE `{tournament_name}_accounts` (" \
                                             "id int AUTO_INCREMENT," \
                                             "mail varchar(128)," \
                                             "password varchar(128)," \
                                             "is_on_uefa int DEFAULT 0," \
                                             "is_at_the_tournament int DEFAULT 0," \
                                             "is_winner int DEFAULT 0," \
                                             "last_message_date date," \
                                             "last_addressee varchar(128)," \
                                             "message_text text," \
                                             "country varchar(256)," \
                                             "champ_club varchar(256)," \
                                             "europe_club varchar(256)," \
                                             "male_club varchar(256)," \
                                             "female_club varchar(256)," \
                                             "is_active int DEFAULT 1," \
                                             "PRIMARY KEY (id)," \
                                             "UNIQUE (mail)" \
                                             ")"
    cursor.execute(create_tournament_accounts_table_query)
    cursor.close()
    database_con.close()


def insert_new_to_base_accounts(mail, password, country, champ_club, europe_club, male_club, female_club):
    database_con, cursor = create_database_connection()
    insert_query = f"INSERT INTO `uefa_base_accounts`" \
                   f" (mail, password, country, champ_club, europe_club, male_club, female_club)" \
                   f" VALUES ('{mail}', '{password}', '{country}', '{champ_club}', '{europe_club}'," \
                   f" '{male_club}', '{female_club}');"
    cursor.execute(insert_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def update_on_uefa_status(mail, tournament_name="example_tournament"):
    database_con, cursor = create_database_connection()
    update_query = f"UPDATE `{tournament_name}_accounts` SET is_on_uefa = 1 WHERE mail = '{mail}';"
    cursor.execute(update_query)
    update_query = f"UPDATE `uefa_base_accounts` SET is_on_uefa = 1 WHERE mail = '{mail}';"
    cursor.execute(update_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def insert_new_to_tournament_accounts(mail, password, country, champ_club,
                                      europe_club, male_club, female_club, tournament_name="example_tournament"):
    database_con, cursor = create_database_connection()

    insert_query = f"INSERT INTO {tournament_name}_accounts (mail, password, country," \
                   f" champ_club, europe_club, male_club, female_club)" \
                   f" VALUES ('{mail}', '{password}', '{country}', '{champ_club}'," \
                   f" '{europe_club}', '{male_club}', '{female_club}');"
    cursor.execute(insert_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def delete_table(table_name):
    database_con, cursor = create_database_connection()
    delete_base_accounts_table_query = f"DROP TABLE `{table_name}`"
    cursor.execute(delete_base_accounts_table_query)
    cursor.close()
    database_con.close()


def create_users_for_management():
    database_con, cursor = create_database_connection()
    create_users_for_management_query = '''CREATE TABLE IF NOT EXISTS `users` (
                                           id INT PRIMARY KEY AUTO_INCREMENT,
                                           username VARCHAR(255) UNIQUE NOT NULL,
                                           password VARCHAR(255) NOT NULL);
                                           '''
    cursor.execute(create_users_for_management_query)
    cursor.close()
    database_con.close()


def create_hetzner_manage_accounts_table():
    database_con, cursor = create_database_connection()
    hetzner_manage_accounts_query = '''CREATE TABLE IF NOT EXISTS `hetzner_manage` (
                                           id INT PRIMARY KEY AUTO_INCREMENT,
                                           email VARCHAR(255) UNIQUE NOT NULL,
                                           password VARCHAR(255) NOT NULL);
                                           '''
    cursor.execute(hetzner_manage_accounts_query)
    cursor.close()
    database_con.close()


def update_hetzner_acc_date(mail, date):
    database_con, cursor = create_database_connection()
    update_query = f"UPDATE `uefa_base_accounts` SET last_message_date = '{date}' WHERE mail = '{mail}';"
    cursor.execute(update_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def update_hetzner_acc_last_msg(mail, msg_text):
    database_con, cursor = create_database_connection()
    msg_text = msg_text.replace("'", '`')
    update_query = f"UPDATE `uefa_base_accounts` SET message_text = '{msg_text}' WHERE mail = '{mail}';"
    cursor.execute(update_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def update_hetzner_acc_addressee(mail, addressee):
    database_con, cursor = create_database_connection()
    update_query = f"UPDATE `uefa_base_accounts` SET last_addressee = '{addressee}' WHERE mail = '{mail}';"
    cursor.execute(update_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def create_clubs_table():
    database_con, cursor = create_database_connection()
    create_clubs_table_query = "CREATE TABLE `clubs` (" \
                                       "id int AUTO_INCREMENT," \
                                       "name varchar(256)," \
                                       "club_type varchar(256)," \
                                       "PRIMARY KEY (id));"
    cursor.execute(create_clubs_table_query)
    cursor.close()
    database_con.close()


def filling_clubs_table(names, club_type):
    database_con, cursor = create_database_connection()

    for name in names:

        insert_query = f"INSERT INTO `clubs` (name, club_type)" \
                       f" VALUES ('{name}', '{club_type}');"
        cursor.execute(insert_query)
    database_con.commit()
    cursor.close()
    database_con.close()


def get_all_countries():
    database_con, cursor = create_database_connection()

    query = f"SELECT * FROM `countries`;"
    cursor.execute(query)
    data = cursor.fetchall()
    database_con.commit()
    cursor.close()
    database_con.close()
    return data


def delete_some_country(country):
    database_con, cursor = create_database_connection()

    query = f"DELETE FROM `countries` WHERE value = '{country}';"
    cursor.execute(query)
    database_con.commit()
    cursor.close()
    database_con.close()


def clubs_transferring():
    database_con, cursor = create_database_connection()
    database_loc_con, loc_cursor = create_database_local_connection()
    loc_cursor.execute("Select * from clubs")
    club_data = loc_cursor.fetchall()
    print(club_data)

    for el in club_data:
        name = el["name"]
        club_type = el["club_type"]
        print(name, club_type)
        cursor.execute(f"INSERT INTO `clubs` (name, club_type) VALUES ('{name}', '{club_type}')")

    database_con.commit()
    cursor.close()
    database_con.close()


def countries_transferring():
    database_con, cursor = create_database_connection()
    database_loc_con, loc_cursor = create_database_local_connection()
    loc_cursor.execute("Select * from countries")
    club_data = loc_cursor.fetchall()
    print(club_data)

    for el in club_data:
        id_ = el["id"]
        value = el["value"]
        print(id_, value)
        cursor.execute(f"INSERT INTO `countries` (id, value) VALUES ('{id_}', '{value}')")

    database_con.commit()
    cursor.close()
    database_con.close()
