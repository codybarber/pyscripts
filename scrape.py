#! usr/bin/env python3
import sys
import praw
import simplejson as json
import pandas as pd
import datetime as dt

now = dt.datetime.now();
today = now.strftime("%Y-%m-%d")
sub = sys.argv[1]
sort = sys.argv[2]

reddit = praw.Reddit(client_id='Zm1SxEqlFurM7w', \
                     client_secret='PkCf97rtrrJcIbTJug899Wa4_r4', \
                     user_agent='progress_pics_2', \
                     username='Nico706', \
                     password='$Cody4u2')

subreddit = reddit.subreddit(sub)
results = []
if sort == 'new':
	results = subreddit.new(limit=1000)
elif sort == 'top':
	results = subreddit.top(limit=1000)
elif sort == 'hot':
	results = subreddit.hot(limit=1000)
else:
	results = subreddit.hot(limit=1000)

topics_dict = { "title":[], \
                "score":[], \
                "permalink": [], \
                "id":[], "url":[], \
                "created": [], \
                "sub": []}

for submission in results:
	if submission.title[0] == 'M' or submission.title[0] == 'F':
		topics_dict["title"].append(submission.title)
		topics_dict["score"].append(submission.score)
		topics_dict["permalink"].append(submission.permalink)
		topics_dict["id"].append(submission.id)
		topics_dict["url"].append(submission.url)
		topics_dict["created"].append(submission.created)
		topics_dict["sub"].append(submission.subreddit)

topics_data = pd.DataFrame(topics_dict)

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def parse_measurements(title):
	if sub == 'brogress':
		string1 = title.replace('[', '|').replace(']', '|').replace('/', '|').replace('>','|').replace('<', '|').replace('-', '|').replace('=','|').replace('to', '|')
		return string1.split('|')
	else:
		string1 = title.replace('[', '|').replace(']', '|').replace('/', '|').replace('>','|').replace('<', '|').replace('-', '|').replace('=','|')
		return string1.split('|')

def parse_gender(measurements):
	if measurements[0]:
		return measurements[0]
	else:
		return ''

def parse_age(measurements):
	if len(measurements) > 1:
		return measurements[1]
	else:
		return ''

def parse_height(measurements):
	if len(measurements) > 2:
		return measurements[2]
	else:
		return ''

def parse_sw(measurements):
	if len(measurements) > 3:
		return measurements[3]
	else:
		return ''

def parse_cw(measurements):
	if len(measurements) > 4:
		return measurements[4]
	else:
		return ''

_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp = _timestamp)

_parsed_title = topics_data["title"].apply(parse_measurements)
topics_data = topics_data.assign(parsed_title = _parsed_title)

_gender = topics_data["parsed_title"].apply(parse_gender)
topics_data = topics_data.assign(gender = _gender)

_age = topics_data["parsed_title"].apply(parse_age)
topics_data = topics_data.assign(age = _age)

_height = topics_data["parsed_title"].apply(parse_height)
topics_data = topics_data.assign(height = _height)

_sw = topics_data["parsed_title"].apply(parse_sw)
topics_data = topics_data.assign(sw = _sw)

_cw = topics_data["parsed_title"].apply(parse_cw)
topics_data = topics_data.assign(cw = _cw)


topics_data.to_csv(today + '_' + sort + '_' + sub + '.csv', index=False) 
