
import feedparser
import datetime
import telebot
import configparser
from bs4 import BeautifulSoup
import requests
import time as t

while True:
	t.sleep(1800)
	config = configparser.ConfigParser()
	config.read ('settings.ini')
	FEED = config.get ('RSS','feed')
	DATETIME = config.get ('RSS','DATETIME')
	BOT_TOKEN = config.get ('Telegram','BOT_TOKEN')
	CHANNEL = config.get ('Telegram','CHANNEL')

	rss = feedparser.parse(FEED)
	bot = telebot.TeleBot(BOT_TOKEN)
	
	for post in reversed(rss.entries):
		data = post.published
		time = datetime.datetime.strptime (data, "%a, %d %b %Y %H:%M:%S %z")
		time_old = config.get ('RSS','datetime')
		time_old = datetime.datetime.strptime(time_old,'%Y-%m-%d  %H:%M:%S%z' )
	
	
		if time <= time_old:
			continue
		else:
			config.set ('RSS','DATETIME', str(time))
			with open ('settings.ini', 'w') as config_file:
				config.write (config_file)
	
		text = post.title
		link = post.link
		url = link
		urlopen = requests.get(url)
		Url = urlopen.text
		soup = BeautifulSoup (Url,'html.parser')
		Images = soup.find("img",class_="img-responsive")
		ImgUrl = "http://kino2.gorodok1.ru" + Images.get("src")
	
		f= open ('out.jpg', 'wb')
		f.write (requests.get(ImgUrl).content)
		f.close()
	
		ImagePic = open ('out.jpg','rb')
	
		bot.send_photo ("-1001093312171",ImagePic)
		bot.send_message(CHANNEL,link + "\n" + text,parse_mode='HTML')


	
	

	

	
