import enum
import praw
from psaw import PushshiftAPI
import pandas as pd
from reddit_settings import getReddit
import datetime as dt
import json
import pprint
import os

try:
    os.mkdir('output')
except Exception as e:
    pass

def get_comments_df(comments):

    results_df = pd.DataFrame()  # create list for results
    reply_df = pd.DataFrame()

    for comment in comments:  # iterate over comments
        try:
            username = comment.author.name
            
        except :
            username =""
        
        item = { #check https://praw.readthedocs.io/en/latest/code_overview/models/comment.html for info about this
            "author": username,
            "body": comment.body,
            "body_html": comment.body_html,
            "created_utc":comment.created_utc,
            "id":comment.id,
            "is_submitter":comment.is_submitter,
            "link_id": comment.link_id,
            "parent_id":comment.parent_id,
            "permalink": comment.permalink,
            "score": comment.score,
            "submission_id": comment.submission.id,
            "subreddit": post.subreddit.display_name,
        }  # create dict from comment
        
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
        "is_self": post.is_self,
        "locked": post.locked,
        "name": post.name,
        "num_comments": post.num_comments,
        "permalink": post.permalink,
        "saved": post.saved,
        "score": post.score,
        "selftext": post.selftext,
        "subreddit": post.subreddit.display_name,
        "title": post.title,
        "upvote_ratio": post.upvote_ratio,
        "url": post.url,
    }

    item_df = pd.Series(item).to_frame()
    item_df = item_df.T

    return item_df

start_time=int(dt.datetime(2021,1,1).timestamp())
end_time=int(dt.datetime(2021,1,2).timestamp())

reddit = getReddit()
api = PushshiftAPI(reddit)
posts = []
submissions_otput_file = 'submissions_output.json'
comments_output_file = 'comments_output.json'


unos = "croatia"

subreddit = reddit.subreddit(unos)


posts=api.search_submissions(
    after = start_time,
    subreddit = unos,
    limit = 3,
    sort ="desc",
    sort_by = "created_utc",
    before = end_time,
    )


submissions_df=pd.DataFrame()


for post in posts:

    comments_df=pd.DataFrame()
    post_df = get_submission_df(post)

    if submissions_df.empty:
        submissions_df=post_df

    else:
        submissions_df=submissions_df.append(post_df)

    comments_df=get_comments_df(post.comments)

    post_id=(post_df.loc[0]["id"])

    filename= "output/comments_for_postid_"+post_id+".csv"
    comments_df.to_csv(filename, index = False)

submissions_df.to_csv ('output/submissions.csv', index = False)

#with open(submissions_otput_file, "w") as outfile: 
 #   json.dump(submissions_dict, outfile)
#with open(comments_output_file, "w") as outfile: 
   # json.dump(comments_dict, outfile)
