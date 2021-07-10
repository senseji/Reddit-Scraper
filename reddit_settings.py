import praw

def getReddit():

    reddit = praw.Reddit(
        client_id='', 
        client_secret='', 
        user_agent='')
    return reddit
