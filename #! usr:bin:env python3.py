#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id='JFlluorMw5yMzQ', \
                     client_secret='Ctrj6NIc40lz-HRMw4RNEc7hcJM ', \
                     user_agent='progress_pics', \
                     username='Nico706', \
                     password='$Cody4u2')

subreddit = reddit.subreddit('progress_pics')

top_subreddit = subreddit.top(limit=500)

topics_dict = { "title":[], \
                "score":[], \
                "id":[], "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[]}

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)