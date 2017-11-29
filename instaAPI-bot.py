#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import atexit
import getpass
import signal
import time
import random
import re
from datetime import datetime
from InstagramAPI import InstagramAPI
try:
	from settings import username, password, hashtag_list, hashtag_blacklist, likes_per_day, min_likes_per_tag, max_likes_per_tag
except:
	username, password = '', ''
	hashtag_list, hashtag_blacklist = [], []
	likes_per_day, min_likes_per_tag, max_likes_per_tag = 0, 0, 0

#parser set up
parser = argparse.ArgumentParser(description='instaAPI-bot - automated likes on instagram')
parser.add_argument('-u', '--username', help='instagram username')
parser.add_argument('-p', '--password', help='instagram password')
parser.add_argument('-l', '--likes', type=int, default=600, help='likes per day')
parser.add_argument('-min', '--minlikes', type=int, default=24, help='min likes per tag round')
parser.add_argument('-max', '--maxlikes', type=int, default=79, help='max likes per tag round')
parser.add_argument('-ht', '--hashtags', nargs='+', default=["l4l", "f4f"], help='hashtags to like')
parser.add_argument('-bl', '--blacklist', nargs='+', default=["sex", "nsfw"], help='blacklist hashtags')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
args = parser.parse_args()

def cleanup(): #logout and exit when CTRL + C is pressed
	InstagramAPI.logout()
	print('\n\n')
	print('Start time: {}'.format(start_time))
	print('Total likes: {}'.format(total_like))
	print('\n\n')

signal.signal(signal.SIGTERM, cleanup)
atexit.register(cleanup)

print('\n\n')
print('instaAPI-bot - automated likes on instagram')
print('-------------------------------------------')
print('\nPress CTRL + C to cancel at any time\n')

#program set up
if args.username:
	username = args.username
if args.password:
	password = args.password
if ((not likes_per_day) and args.likes):
	likes_per_day = args.likes
else:
	while not likes_per_day:
		print('likes per day must be > 0')
		try:
			likes_per_day = int(input('\nLikes per day: '))
		except:
			pass
if not min_likes_per_tag:
	min_likes_per_tag = args.minlikes
if not max_likes_per_tag:
	max_likes_per_tag = args.maxlikes
if not hashtag_list:
	hashtag_list = args.hashtags
if not hashtag_blacklist:
	hashtag_blacklist = args.blacklist
if not username:
	username = input('Instagram username: ')
if not password:
	password = getpass.getpass('Instagram password: ')

#login
InstagramAPI = InstagramAPI(username, password)
print('Please wait...')
if not InstagramAPI.login():
	print('Wrong username / password')
	exit(0)

#display values
print('\nCheck if everything looks alright->')
print('Username: {}'.format(username))
print('Likes per day: {}'.format(likes_per_day))
print('Likes per tag round: between {} and {}'.format(min_likes_per_tag,max_likes_per_tag))
print('Hashtag list: {}'.format(hashtag_list))
print('\nPress CTRL + C to cancel at any time')
wait_to_start = random.randint(20,30)
print('Programm starts in {} seconds...\n'.format(wait_to_start))
time.sleep(wait_to_start)

total_like = 0
waiting_time = (60 * 60 * 24) / likes_per_day
start_time = datetime.now().strftime('%A, %d. %B %Y %I:%M%p')

#program start
while True:
	print('\nLoading pictures...')
	round_like = 0
	while True:
		random_tag = random.choice(hashtag_list)
		try:
			InstagramAPI.tagFeed(random_tag)
			break
		except:
			time.sleep(random.randint(2,4))

	media_id = InstagramAPI.LastJson

	likes_per_tag = random.randint(min_likes_per_tag,max_likes_per_tag)
	for element in media_id['items'][:likes_per_tag]:
		if not element['caption']['text']:
			print('No caption')
			continue
		for hashtag in re.split(r'#|\s', element['caption']['text']): #blacklist
			if hashtag.strip().lower() in hashtag_blacklist:
				print('Blacklisted hashtag "{}" found, skipping...'.format(hashtag))
				break #blacklist hashtag found
		else:
			print("Liking picture ID {} in #{}...".format(element['pk'], random_tag))
			try:
				InstagramAPI.like(element['pk'])
			except:
				print('Picture has been removed, skipping...')
				time.sleep(random.randint(2,4))
				continue
			round_like += 1
			total_like += 1
			print("Current round like: {}, total like: {}".format(round_like, total_like))
			random_sec = random.randint(2,24)
			print("Waiting {} seconds...\n".format(int(waiting_time + random_sec)))
			time.sleep(waiting_time + random_sec)