# Reddit-Scraper
Scraper for Reddit, gathering posts and comments, outputting it as .csv files.


* Evaluates if contents of posts and comments contain any value from keywords.txt
* Plots how many comments have keyword value in them
* Outputs submissions.csv, comments.csv
* Outputs comments by id in comment/ directory


## Preparing the enviroment

1.  '''pip install -r requirements.txt'''
2.  In reddit_settings.py, insert your credentials obtained after creating Reddit API token.
3.  Adjust 'subreddit', 'start_time','end_time' to your liking
