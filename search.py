import mysql.connector
from mysql.connector import errorcode

USERNAME = input("MySQL username:")
PASSWORD = input("Password:")
key_word = input("The theme you are interested in:")
# 打开数据库连接
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD, database = 'twitter_data')
# 使用cursor()方法获取操作游标
cursor = cnx.cursor()
cursor.execute("SELECT cont_no FROM contents WHERE cont_name = '"+key_word+"'")
cont_no = cursor.fetchall()[0][0]
cursor.execute("SELECT pic_no FROM twitter_data WHERE cont_no = '"+str(cont_no)+"'")
pic_nos = cursor.fetchall()
twit_nos = set()
for pic_no in pic_nos:
    cursor.execute("SELECT twit_no FROM pictures WHERE pic_no = '"+str(pic_no[0])+"'")
    twitter_no = cursor.fetchall()
    twitter_nos.add(twit_no[0][0])
for twit_no in twit_nos:
    cursor.execute("SELECT twit_name FROM twitters WHERE twit_no = '"+str(twit_no)+"'")
    print(cursor.fetchall()[0][0])
cursor.close()
cnx.close()
