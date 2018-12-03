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
from google.cloud import videointelligence
import io

  
#consumer_key = '..............'
#consumer_secret = '.............'
#access_token = '..............'
#access_secret = '...............'




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
    #urllib.request.urlretrieve(line, str(file_count)+".jpg")

cnx.commit()
cursor.close()
cnx.close()


os.system('ffmpeg -loglevel panic -framerate 0.4 -i images/%d.jpg -c:v libx264 -r 30 -s 800*600 -pix_fmt yuv420p video.mp4')


video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
with io.open("video.mp4", 'rb') as movie:
    video = movie.read()
operation = video_client.annotate_video(features=features, input_content=video)
print('\nProcessing video for label annotations:')
result = operation.result(timeout=90)
print('\nFinished processing.')

# first result is retrieved because a single video was processed

#segment_labels = result.annotation_results[0].segment_label_annotations
#for i, segment_label in enumerate(segment_labels):
#    print('Video label description: {}'.format(
#        segment_label.entity.description))
#    for category_entity in segment_label.category_entities:
#        print('\tLabel category description: {}'.format(
#            category_entity.description))
#
#    for i, segment in enumerate(segment_label.segments):
#        start_time = (segment.segment.start_time_offset.seconds +
#                      segment.segment.start_time_offset.nanos / 1e9)
#        end_time = (segment.segment.end_time_offset.seconds +
#                    segment.segment.end_time_offset.nanos / 1e9)
#        positions = '{}s to {}s'.format(start_time, end_time)
#        confidence = segment.confidence
#        print('\tSegment {}: {}'.format(i, positions))
#        print('\tConfidence: {}'.format(confidence))
#    print('\n')


#shot_labels = result.annotation_results[0].shot_label_annotations
#for i, shot_label in enumerate(shot_labels):
#    print('Video label description: {}'.format(
#        shot_label.entity.description))
#    for category_entity in shot_label.category_entities:
#        print('\tLabel category description: {}'.format(
#            category_entity.description))
#
#    for i, shot in enumerate(shot_label.segments):
#        start_time = (shot.segment.start_time_offset.seconds +
#                      shot.segment.start_time_offset.nanos / 1e9)
#        end_time = (shot.segment.end_time_offset.seconds +
#                    shot.segment.end_time_offset.nanos / 1e9)
#        positions = '{}s to {}s'.format(start_time, end_time)
#        confidence = shot.confidence
#        print('\tSegment {}: {}'.format(i, positions))
#        print('\tConfidence: {}'.format(confidence))
#    print('\n')
#

shot_labels = result.annotation_results[0].shot_label_annotations
file = open('label_annotation_list.txt', 'w')

label_count = 0
cont_name = []
for i, shot_label in enumerate(shot_labels):
    cont_name.append(shot_label.entity.description)
    label_count += 1
    file.write('    ' + str(label_count) + '\t{}'.format(shot_label.entity.description) + '\n')
cont_no = list(range(1,label_count+1))

# connect to database
cnx = mysql.connector.connect(user = USERNAME, password = PASSWORD, database = 'lxy_mini3')
cursor = cnx.cursor()

# insert data
add_content = ("INSERT IGNORE INTO contents "
              "(cont_no, cont_name) "
              "VALUES (%s, %s)")
add_pic_content = ("INSERT IGNORE INTO twitter_datas "
              "(pic_no, cont_no) "
              "VALUES (%s, %s)")
for i in range(label_count):
    cursor.execute("SELECT MAX(cont_no) FROM contents")
    content_start_id = cursor.fetchall()[0][0]
    if content_start_id == None:
        content_start_id = 0
    data_content = (content_start_id+1, cont_name[i])
    cursor.execute(add_content, data_content)
    cnx.commit()

for i, shot_label in enumerate(shot_labels):
    file.write('Video label description: {}'.format(shot_label.entity.description) + '\n')
    cursor.execute("SELECT * FROM contents WHERE cont_name = '"+cont_name[i]+"'")
    current_row_id = cursor.fetchall()[0][0]
    for category_entity in shot_label.category_entities:
        file.write('\tLabel category description: {}'.format(category_entity.description) + '\n')
    for i, shot in enumerate(shot_label.segments):
        start_time = (shot.segment.start_time_offset.seconds +
                      shot.segment.start_time_offset.nanos / 1e9)
        end_time = (shot.segment.end_time_offset.seconds +
                    shot.segment.end_time_offset.nanos / 1e9)

        frame_no = int(round(end_time*0.4))
        data_pic_content = (pic_start_id+frame_no, current_row_id)
        cursor.execute(add_pic_content, data_pic_content)
        positions = '{}Picture number {}'.format('', frame_no)
        confidence = shot.confidence
        file.write('\tSegment {}: {}'.format(i+1, positions) + '\n')
        file.write('\tConfidence: {}'.format(confidence) + '\n')
    file.write('\n')
file.close()
cnx.commit()
cursor.close()
cnx.close()
