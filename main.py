#######
# IMPORT PACKAGES
#######

import os
import platform
import logging
from pmaw import PushshiftAPI
from datetime import datetime

# Get important info
if platform.system() == 'Windows':
    thread_count = os.cpu_count() * 2
else:
    thread_count = len(os.sched_getaffinity(0)) * 2  # Get the number of threads

date_start = int(datetime(2022, 2, 1, 0, 0).timestamp())
date_end = int(datetime(2022, 2, 1, 5, 0).timestamp())

post_limit = 100
comment_limit = 500

# Set up the logger
if not os.path.exists('logs'):
    os.mkdir('logs')
log_name = datetime.now().strftime('logs/reddit-scraper-%Y-%m-%d-%H-%M-%S.log')
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s',
    filename=log_name, filemode='w'
)


def log(message, level=logging.INFO):
    logging.log(level, message)


# Access the PushShift Reddit API
api = PushshiftAPI(
    num_workers=thread_count
)

# later list ['Flash', 'FlashArchival', 'FlashPlayer', 'FlashPlayerForever']
subreddits = ['AdobeFlash']  # make a list of subreddits you want to scrape the data from

for subreddit in subreddits:
    posts = api.search_submissions(
        subreddit=subreddit,
        limit=post_limit
    )

    post_ids = [post['id'] for post in posts]
    comment_ids = api.search_submission_comment_ids(post_ids)

    comments = api.search_comments(ids=comment_ids)
