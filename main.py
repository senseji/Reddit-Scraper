import praw
from psaw import PushshiftAPI
import pandas as pd
from reddit_settings import getReddit
import datetime as dt
import pprint
import json

def comments_to_dicts(comments):

    results = []  # create list for results
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
            "distinguished":comment.distinguished,
            "edited":comment.edited,
            "id":comment.id,
            "is_submitter":comment.is_submitter,
            "link_id": comment.link_id,
            "parent_id":comment.parent_id,
            "permalink": comment.permalink,
            "saved": comment.saved,
            "score": comment.score,
            "stickied": comment.stickied,
            "submission_id": comment.submission.id,
            "subreddit": post.subreddit.display_name,

        }  # create dict from comment

        if len(comment._replies) > 0:
            item["replies"] = comments_to_dicts(comment._replies)  # convert replies using the same function

        results.append(item)  # add converted item to results 
    return results  # return all converted comments

def submission_to_dicts(post):
    try:
        username = post.author.name
    except :
        username =""

    item = {
        "author": username,
        "clicked": post.clicked,
        "created_utc": post.created_utc,
        "distinguished": post.distinguished,
        "edited": post.edited,
        "id": post.id,
        "is_original_content": post.is_original_content,
        "is_self": post.is_self,
        "link_flair_template_id": post.link_flair_template_id,
        "link_flair_text": post.link_flair_text,
        "locked": post.locked,
        "name": post.name,
        "num_comments": post.num_comments,
        "over_18": post.over_18,
        "permalink": post.permalink,
        "saved": post.saved,
        "score": post.score,
        "selftext": post.selftext,
        "spoiler": post.spoiler,
        "stickied": post.stickied,
        "subreddit": post.subreddit.display_name,
        "title": post.title,
        "upvote_ratio": post.upvote_ratio,
        "url": post.url,

    }

    return item



start_time=int(dt.datetime(2021,1,1).timestamp())
end_time=int(dt.datetime(2021,1,2).timestamp())

reddit = getReddit()
api = PushshiftAPI(reddit)
posts = []
submissions_otput_file = 'submissions_output.json'
comments_output_file = 'comments_output.json'


unos = input("Unesi ime subreddita (npr 'learnpython'):")

subreddit = reddit.subreddit(unos)

posts=list(api.search_submissions(
    after = start_time,
    subreddit = unos,
    limit = 3,
    sort ="asc",
    sort_by = "created_utc",
    #before = end_time,
    ))
submissions_dict=[]
comments_dict=[]
for post in posts:

    submissions_dict.append(submission_to_dicts(post))
    comments_dict.append(comments_to_dicts(post.comments))

with open(submissions_otput_file, "w") as outfile: 
    json.dump(submissions_dict, outfile)

with open(comments_output_file, "w") as outfile: 
    json.dump(comments_dict, outfile)
