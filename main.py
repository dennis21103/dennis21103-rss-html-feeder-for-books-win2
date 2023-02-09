#!/usr/bin/python3
# Get from by Yevgeniy Goncharov, https://sys-adm.in/programming/805-rss-fider-na-python-s-opravkoj-uvedomlenij-v-telegram.html,
# Script for reading and forwarding to Telegram(not used for me), rss feeds

# Imports
import sqlite3
import requests
import feedparser
import os
import urllib
import random

# Bot creds
#bot_token = 'TOKEN'
#bot_chatID = 'CHAT_ID'

# Feeds
myfeeds = [
  'https://forum.sys-adm.in/latest.rss',
  #  'https://readmanga.live/rss/manga?name=o_moem_pererojdenii_v_mech',
]
# 0 = .
# 8 = -
# Написать функцию зманеы входных символов на 0 и 8 по шаблону
tablename: str = 'forum0sys8ad_m0in'
rss = 'False'

# User agents
uags = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

# Random User Agent (from uags list)
ua = random.choice(uags)

# Header
headers = {
  "Connection" : "close",  # another way to cover tracks
  "User-Agent" : ua
}

# Proxies
proxies = {
}

# DB
scriptDir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(scriptDir + '/db/rss.sqlite')
db = db_connection.cursor()
#dbline = 'CREATE TABLE IF NOT EXISTS '+ tablename + '(title TEXT, date TEXT)'
#query = NULL
query = 'CREATE TABLE IF NOT EXISTS {} '.format(tablename)
query: str = query + '(title TEXT, date TEXT, read TEXT, rss TEXT, link TEXT, message TEXT)'

#'CREATE TABLE IF NOT EXISTS myrss (title TEXT, date TEXT)'
db.execute(query)

# Get posts from DB and print
def get_posts():
    with db_connection:
        db.execute("SELECT * FROM myrss")
        print(db.fetchall())

# Check post in DB
def article_is_not_db(article_title, article_date):
    query = 'SELECT * from {} '.format(tablename)
    query = query + 'WHERE title=? AND date=?'
    db.execute(query, (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

# Add post to DB
def add_article_to_db(article_title, article_date, article_rss, article_link, article_message):
    read: str = 'False'
    query = 'INSERT INTO {} '.format(tablename)
    query = query + 'VALUES (?,?,?,?,?,?)'
    db.execute(query, (article_title, article_date, read, article_rss, article_link, article_message))
    db_connection.commit()

# Send notify to Telegram bot
#def bot_sendtext(bot_message):
#    bot_message = urllib.parse.quote(bot_message)
#    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
#    requests.get(send_text, proxies=proxies, headers=headers)
#   print(send_text)

# Check, read articles
def read_article_feed(feed):
    """ Get articles from RSS feed """
    feedparser.USER_AGENT = ua
    feed = feedparser.parse(feed)
    print(feed)
    if 'bozo_exception' in feed:
        a :str = feed['bozo_exception']
        b:str = str(feed.bozo)
        if  b != 'False':
            print ('problem with URL',' error ',a )
    return 0
    for article in feed['entries']:
        if article_is_not_db(article['title'], article['published']):
            rss: str = feed['version']
            add_article_to_db(article['title'], article['published'], rss, article['link'], article['summary'])
            #bot_sendtext('New feed found ' + article['title'] + ', ' + article['link'] + ', ' + article['description'])
            print(article)

# Rotate feeds array
def spin_feds():
    for x in myfeeds:
        print(x)
        read_article_feed(x)

# Runner :)
if __name__ == '__main__':
    spin_feds()
    # get_posts()
    db_connection.close()
