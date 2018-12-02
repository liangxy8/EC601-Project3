from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'twitter_data'

TABLES = {}
TABLES['twitters'] = (
    "CREATE TABLE `twitters` ("
    "  `twit_no` int(11) NOT NULL,"
    "  `twit_name` varchar(20) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`twit_no`)"
    ") ENGINE=InnoDB")

TABLES['contents'] = (
    "CREATE TABLE `contents` ("
    "  `cont_no` int(11) NOT NULL,"
    "  `cont_name` varchar(20) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`cont_no`)"
    ") ENGINE=InnoDB")

TABLES['pictures'] = (
    "CREATE TABLE `pictures` ("
    "  `pic_no` int(11) NOT NULL,"
    "  `pic_url` varchar(40) NOT NULL UNIQUE,"
    "  `twit_no` int(11) NOT NULL,"
    "  FOREIGN KEY (`twit_no`) REFERENCES `twitters` (`twit_no`) ON DELETE CASCADE, "
    "  PRIMARY KEY (`pic_no`)"
    ") ENGINE=InnoDB")

TABLES['twitter_datas'] = (
    "CREATE TABLE `twitter_datas` ("
    "  `pic_no` int(11) NOT NULL,"
    "  `cont_no` int(11) NOT NULL,"
    "  FOREIGN KEY (`pic_no`) REFERENCES `pictures` (`pic_no`) ON DELETE CASCADE, "
    "  FOREIGN KEY (`cont_no`) REFERENCES `contents` (`cont_no`) ON DELETE CASCADE"
    "  PRIMARY KEY (`pic_no`,`cont_no`), KEY `pic_no` (`pic_no`),"
    "  KEY `cont_no` (`cont_no`),"
    ") ENGINE=InnoDB")

USERNAME = input("MySQL username: \n")
PASSWORD = input("Password: \n")
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD)
cursor = cnx.cursor()
cursor.execute("DROP DATABASE "+DB_NAME)



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
