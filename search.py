import mysql.connector
from mysql.connector import errorcode
import sys

USERNAME = input("MySQL username:")
PASSWORD = input("Password:")
key_word = input("The theme you are interested in:")
# 打开数据库连接
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD, database = 'lxy_mini3')
# 使用cursor()方法获取操作游标
cursor = cnx.cursor()
cursor.execute("SELECT cont_no FROM contents WHERE cont_name = '"+key_word+"'")
try:
    cont_no = cursor.fetchall()[0][0]
except IndexError:
    print('no user had {} in their sessions'.format(key_word))
    sys.exit()
cursor.execute("SELECT pic_no FROM twitter_datas WHERE cont_no = '"+str(cont_no)+"'")
pic_nos = cursor.fetchall()
print("pic_nos is:", pic_nos)
twitter_nos = set()
print("twitter_nos is:", twitter_nos)

for pic_no in pic_nos:
    cursor.execute("SELECT twit_no FROM pictures WHERE pic_no = '"+str(pic_no[0])+"'")
    twitter_no = cursor.fetchall()
    twitter_nos.add(twitter_no[0][0])
for twitter_no in twitter_nos:
    cursor.execute("SELECT twit_name FROM twitters WHERE twit_no = '"+str(twitter_no)+"'")
    print(cursor.fetchall()[0][0])
cursor.close()
cnx.close()
