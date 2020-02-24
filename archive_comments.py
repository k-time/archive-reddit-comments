import argparse
from collections import OrderedDict
import json
import logging
import praw
import sys
import time
import yaml

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('DELETE_COMMENTS')

# Load configs
with open('config.yaml', 'r') as cfg_file:
    cfg = yaml.load(cfg_file)


def connect():
    # Authentication
    return praw.Reddit(
            client_id=cfg['client_id'],
            client_secret=cfg['client_secret'],
            user_agent=cfg['user_agent'],
            username=cfg['username'],
            password=cfg['pw'])


def get_file_path():
    # Command-line options parser
    parser = argparse.ArgumentParser(description='Archives Reddit comments.')
    parser.add_argument('-p', '--path', dest='path', help='Set the path for the exported file.')
    args = parser.parse_args()

    if args.path is not None:
        path = args.path
        if not path.endswith("/") and not path.endswith("\\"):
            if "\\" in path:
                path += "\\"
            else:
                path += "/"
        return path + cfg['default_file_name']
    else:
        return cfg['default_file_name']


def export_comments(reddit):
    file_path = get_file_path()
    logger.info("Saving all comments to file \"%s\"...", file_path)
    try:
        file = open(file_path, 'a+')
        fields = ('subreddit_name_prefixed', 'link_title', 'link_id', 'link_url', 'name',
                  'id', 'parent_id', 'created', 'created_utc', 'permalink', 'score', 'body')
        comment_list = []
        # Reddit PRAW API only allows you to retrieve last 1000 comments; TBD when they will allow all
        for comment in reddit.redditor(cfg['username']).comments.new(limit=None):
            if comment.body == "[deleted]":
                continue
            comment_dict = vars(comment)
            sub_dict = OrderedDict()
            for field in fields:
                sub_dict[field] = comment_dict[field]
            sub_dict['permalink'] = 'https://www.reddit.com' + sub_dict['permalink']
            # Convert time to readable timestamp
            sub_dict['local_time'] = time.strftime('%Y-%m-%d %I:%M:%S %p EST', time.localtime(sub_dict['created_utc']))
            comment_list.append(sub_dict)

        json_string = json.dumps(comment_list, indent=4)
        file.write(json_string)
        file.close()

    except OSError:
        logger.info("Unable to create file \"%s\". Please check that the file path is valid.", file_path)


def overwrite_comments(reddit):
    logger.info("Overwriting all comments (this may take a few minutes)...")
    for comment in reddit.redditor(cfg['username']).comments.new(limit=None):
        if comment.body != "[deleted]":
            comment.edit("[deleted]")


def main():
    reddit = connect()
    logger.info("Logged in as user \"u/%s\"...", cfg['username'])
    export_comments(reddit)
    overwrite_comments(reddit)
    logger.info("Finished successfully!")


if __name__ == '__main__':
    main()
