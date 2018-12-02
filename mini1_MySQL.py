#!/usr/bin/env python

import tweepy
from tweepy import OAuthHandler
import wget
import json
import argparse
import os
import mysql.connector
from mysql.connector import errorcode
import urllib

  
#consumer_key = '..............'
#consumer_secret = '.............'
#access_token = '..............'
#access_secret = '...............'


consumer_key = 'dEqh76HwX5U7hCIK2iIcxoxru'
consumer_secret = '5K20dpFlGIkyKZjqGBEshKafHq39ac2ThARhe1Uf1gPLNIBJfx'
access_token = '1041005266832121858-n8UPtUdnEHLAwZKaJYL22bR7v4DdFA'
access_secret = 'ShaAqtOZnyeyoC7GEx8ewPSiFXmMM2irlPmPAOwCjBjlT'


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def parse_arguments():
  parser = argparse.ArgumentParser(description='Download pictures from Twitter.')
  parser.add_argument('--username',type=str , help='the twitter screen name from the account we want to retrieve all the picture')
  parser.add_argument('--num', type=int, default=100, help='Maximum number of tweets to be returned.')
  parser.add_argument('--output', default='pictures/', type=str, help='folder where the pictures will be stored')
  args = parser.parse_args()
  return args


def create_folder(output_folder):
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def tweet_media_urls(tweet_status):
  media = tweet_status._json.get('extended_entities', {}).get('media', [])
  if (len(media) == 0):
    return []
  else:
    return [item['media_url'] for item in media]


def download_images_by_user(api, username, num_tweets, output_folder):
    status = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items()
    create_folder(output_folder)
    downloaded = 0
    file = open("image_list.txt", 'w')
    for tweet_status in status:
        if(downloaded >= num_tweets):
            break
        i = 0
        for media_url in tweet_media_urls(tweet_status):
            file_name = str(downloaded) + ".jpg"
            if True or (not os.path.exists(os.path.join(output_folder, file_name))):
                wget.download(media_url, out=output_folder+'/'+file_name)
                downloaded += 1
                #print(media_url)
                file.write(str(media_url)+'\n')
    file.close()


arguments = parse_arguments()
username = arguments.username
num_tweets = arguments.num
output_folder = arguments.output
download_images_by_user(api, username, num_tweets, output_folder)

f = open("image_list.txt").readlines()

# Connect to the MySQL server
USERNAME = input("MySQL username: \n")
PASSWORD = input("Password: \n")
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD, database = 'lxy_mini3')
cursor = cnx.cursor()

# Inserting new data by using the handler structure cursor
add_twitter = ("INSERT INTO twitters "
                   "(twit_no, twit_name) "
                   "VALUES (%s, %s)")
cursor.execute("SELECT MAX(twit_no) FROM twitters")
twitter_start_id = cursor.fetchall()[0][0]
if twitter_start_id == None:
    twitter_start_id = 0
data_twitter = (twitter_start_id+1, username)
cursor.execute(add_twitter, data_twitter)

cursor.execute("SELECT * FROM twitters WHERE twit_name = '"+username+"'")
current_row_id = cursor.fetchall()[0][0]

add_pic = ("INSERT INTO pictures "
                   "(pic_no, twit_no, pic_url) "
                   "VALUES (%s, %s, %s)")

file_count = 0
pic_start_id = 0
for line in f:
    cursor.execute("SELECT MAX(pic_no) FROM pictures")
    pic_start_id = cursor.fetchall()[0][0]
    if pic_start_id == None:
        pic_start_id = 0
    data_pic = (pic_start_id+1, current_row_id, line)
    cursor.execute(add_pic, data_pic)
    file_count += 1
    urllib.request.urlretrieve(line, str(file_count)+".jpg")

cnx.commit()
cursor.close()
cnx.close()
