import praw

def getReddit():

    reddit = praw.Reddit(
        client_id='yezlsT_S-LplPbDOT8Q9rw', 
        client_secret='fS8KXBfnhFTPDJw74oXriq2vi2_GrA', 
        user_agent='SCRAPER')
    return reddit