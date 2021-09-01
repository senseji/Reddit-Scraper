import enum
import praw
from psaw import PushshiftAPI
import pandas as pd
from reddit_settings import getReddit
import datetime as dt
import json
import pprint
import os
from tqdm import tqdm
from datetime import datetime
import csv
from matplotlib import pyplot



try:
    os.mkdir('output')
except Exception as e:
    pass

try:
    os.mkdir('output/comments')
except Exception as e:
    pass

def get_comments_df(comments):

    results_df = pd.DataFrame()  # create list for results
    reply_df = pd.DataFrame()

    for comment in comments:  # iterate over comments
    
        if not(isinstance(comment,praw.models.MoreComments)):
            try:
                username = comment.author.name
                
            except :
                username =""
            
            try:
                body = comment.body
                
            except :
                body =""
            
            item = { #check https://praw.readthedocs.io/en/latest/code_overview/models/comment.html for info about this
                "author": username,
                "body": body,
                "id":comment.id,
                "link_id": comment.link_id,
                "parent_id":comment.parent_id,
                "score": comment.score,
                "submission_id": comment.submission.id,

            }  # create dict from comment
            item["datetime"]=datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            item_df = pd.Series(item).to_frame()
            item_df = item_df.T

            if len(comment._replies) > 0:
                reply_df = get_comments_df(comment._replies)  # convert replies using the same function
                item_df = item_df.append(reply_df)

            results_df=results_df.append(item_df)  # add converted item to results 

    return results_df  # return all converted comments

def get_submission_df(post):
    try:
        username = post.author.name
    except :
        username =""

    item = {
        "author": username,
        "created_utc": post.created_utc,
        "id": post.id,
        "name": post.name,
        "num_comments": post.num_comments,
        "selftext": post.selftext,
        "subreddit": post.subreddit.display_name,
        "title": post.title,
        "upvote_ratio": post.upvote_ratio,
        "url": post.url,
    }
    item["datetime"]=datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')

    item_df = pd.Series(item).to_frame()
    item_df = item_df.T

    return item_df

start_time=int(dt.datetime(2021,5,31).timestamp())
end_time=int(dt.datetime(2021,2,1).timestamp())
keywords=[]

with open('keywords.txt',encoding="utf8") as fd:
    lines = fd.read().split(',')
    for line in lines:
        keywords.append(line.replace(" ","").replace("'",""))


reddit = getReddit()
api = PushshiftAPI(reddit)
posts = []
submissions_otput_file = 'submissions_output.json'
comments_output_file = 'comments_output.json'


unos = "croatia"

subreddit = reddit.subreddit(unos)


posts=api.search_submissions(
    before = start_time,
    subreddit = unos,
    limit = 1000,
    sort ="desc",
    sort_by = "created_utc",
    after = end_time,
    )


submissions_df=pd.DataFrame()
all_comments_df=pd.DataFrame()

for post in tqdm(posts):
    comments_df=pd.DataFrame()
    post_df = get_submission_df(post)

    if submissions_df.empty:
        submissions_df=post_df

    else:
        submissions_df=submissions_df.append(post_df)

    comments_df=get_comments_df(post.comments)
    try:
        comments_df["korona_sadrzaj"]=comments_df['body'].apply(lambda x: any([k in x for k in keywords])).astype(int)
    except:
        pass

    all_comments_df=all_comments_df.append(comments_df)
    post_id=(post_df.loc[0]["id"])

    filename= "output/comments/comments_for_postid_"+post_id+".csv"
    comments_df.to_csv(filename, index = False)


namebools=submissions_df["name"].apply(lambda x: any([k in x for k in keywords]))
textbools=submissions_df["selftext"].apply(lambda x: any([k in x for k in keywords]))

submissions_df["korona_sadrzaj"]=(namebools | textbools).astype(int)
submissions_df["korona_cumsum"]=submissions_df["korona_sadrzaj"].cumsum()
all_comments_df["korona_cumsum"]=all_comments_df["korona_sadrzaj"].cumsum()

submissions_df.reset_index(drop=True,inplace=True)
all_comments_df.reset_index(drop=True,inplace=True)
submissions_df.reset_index(inplace=True)
all_comments_df.reset_index(inplace=True)


all_comments_df.to_csv('output/all_comments.csv', index = False)
submissions_df.to_csv('output/all_submissions.csv', index = False)

print(submissions_df)

all_comments_df.plot.scatter(x='datetime',y='index')
all_comments_df.plot.scatter(x='datetime',y='korona_cumsum')
pyplot.show()




