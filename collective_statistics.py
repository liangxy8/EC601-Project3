import mysql.connector
from mysql.connector import errorcode
USERNAME = input("MySQL username:")
PASSWORD = input("password:")
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD, database = 'lxy_mini3')
cursor = cnx.cursor()
cursor.execute("SELECT cont_no FROM contents")
cont_nos = cursor.fetchall()
content_count = 0
for cont_no in cont_nos:
    cursor.execute("SELECT COUNT(*) FROM twitter_datas WHERE cont_no = '"+str(cont_no[0])+"'")
    count = cursor.fetchall()[0][0]
    if count >= content_count:
        content_count = count

for cont_no in cont_nos:
    cursor.execute("SELECT COUNT(*) FROM twitter_datas WHERE cont_no = '"+str(cont_no[0])+"'")
    count = cursor.fetchall()[0][0]
    if count >= content_count:
        cursor.execute("SELECT cont_name FROM contents WHERE cont_no = '"+str(cont_no[0])+"'")
        cont_name = cursor.fetchall()[0][0]
        print("The most popular tag is {}, which appears {} times".format(cont_name, count))

cursor.execute("SELECT twit_no FROM twitters")
twit_nos = cursor.fetchall()
for twit_no in twit_nos:
    cursor.execute("SELECT twit_name FROM twitters WHERE twit_no = '"+str(twit_no[0])+"'")
    twit_name = cursor.fetchall()[0][0]
    cursor.execute("SELECT COUNT(*) FROM pictures WHERE twit_no = '"+str(twit_no[0])+"'")
    count = cursor.fetchall()[0][0]
    print("There are {} pictures collected from {} in your database. ".format(count, twit_name))
cursor.close()
cnx.close()
