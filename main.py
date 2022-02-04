#######
# IMPORT PACKAGES
#######

import os
import platform
import logging
from math import floor
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
max_log_files = 25

# Set up the logger
if not os.path.exists('logs'):
    os.mkdir('logs')
else:
    # Ensure we don't have too many log files
    log_files = os.listdir('logs')
    if len(log_files) > max_log_files:
        os.remove(f'logs/{log_files[0]}')

logger = None
while True:
    log_name = datetime.now().strftime('logs/reddit-scraper-%Y-%m-%d-%H-%M-%S.log')
    format_string = '[%(levelname)-10s] [%(threadName)s] [%(name)-14s] - %(message)s'
    formatter = logging.Formatter(format_string)
    handler = logging.FileHandler(log_name)
    handler.setFormatter(formatter)

    logging.basicConfig(format=format_string, force=True)
    logger = logging.getLogger("Reddit Scraper")
    logger.addHandler(handler)
    break


def log(message, level=logging.INFO):
    logger.log(level, f'{message}')


# Access the PushShift Reddit API
api = PushshiftAPI(
    num_workers=thread_count
)

log(f'Initialized the PMAW scraper with {thread_count} threads')
log(f'Post limit per fetch is {post_limit}')
log(f'Comment limit per fetch is {comment_limit}')

# TODO: Initialize a SQLite database
# TODO: Get the list of subreddits from the database
# later list ['Flash', 'FlashArchival', 'FlashPlayer', 'FlashPlayerForever']
subreddits = ['AdobeFlash']  # make a list of subreddits you want to scrape the data from


def end_time(start, message):
    end = datetime.now()
    difference = end - start
    log(f'It took {floor(difference.seconds / 60)} m {difference.seconds % 60} s to {message}')


for subreddit in subreddits:
    start = datetime.now()
    log(f'Gathering posts for r/{subreddit} subreddit')
    posts = api.search_submissions(subreddit=subreddit, limit=post_limit)
    post_count = len(posts)
    log(f'Gathered {post_count} posts for r/{subreddit} subreddit')
    end_time(start, 'get posts')

    start = datetime.now()
    log(f'Gathering comment ids for {post_count} posts for r/{subreddit} subreddit')
    post_ids = [post['id'] for post in posts]
    comment_ids = api.search_submission_comment_ids(post_ids, limit=comment_limit)
    comment_count = len(comment_ids)
    log(f'Gathered {comment_count} comment ids for {post_count} posts for r/{subreddit} subreddit')
    end_time(start, 'get comment ids')

    start = datetime.now()
    log(f'Gathering {comment_count} comments for {post_count} posts for r/{subreddit} subreddit')
    comments = api.search_comments(ids=comment_ids, limit=comment_limit)
    log(f'Gathered {comment_count} comments for {post_count} posts for r/{subreddit} subreddit')
    end_time(start, 'get comments')
