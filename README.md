# EC601-Project3
## Before you use database
1. Install MySQL and MongoDB database following the tutorial
2. Install MySQL-python connector
3. Add your own json file to system environment (for example):
   ```python
   $ export GOOGLE_APPLICATION_CREDENTIALS="/home/lxy/EC601/EC601-Project3/mini-project3-6e29c4fa21eb.json"
   ```
## How to use this project
1. Apply a MySQL account and run ___create_database.py___.
   The function of ___create_database.py___ is to create a database named ___lxy_mini3___, and I established 4 tables:
|    | Tables_in_lxy_mini3  |    |
| -- |:--------------------:| --:|
|    | contents             |    |
|    | pictures             |    |
|    | twitter_datas        |    |
|    | twitters             |    |
2. Run the program ___mini1_MySQL.py___ using the following format:
   ```python
   $ python mini1_MySQL.py --username [the twitter you'd like to search] --num [the number of twitter you want to get] --output [the name of the output folder]
   ```
   for example:
   ```python
   $ python mini1_MySQL.py --username NatGeo --num 20 --output './images/'
   ```
   and then the data will be saved in your database.
3. Run the program ___search.py___ and input the theme you are interested in. Then you can get results of which user had the theme in their sessions.
4. Run the program ___collective_statistics.py___. Then the results will show you the most popular descriptors in your database and the number of images per feed.


