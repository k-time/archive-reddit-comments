import argparse
from collections import OrderedDict
import json
import logging
from pprint import pprint
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
    parser = argparse.ArgumentParser(description='Reddit bot that searches and posts MMA scorecards.')
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
        fields = (
            'subreddit_name_prefixed',
            'link_title',
            'link_id',
            'link_url',
            'name',
            'id',
            'parent_id',
            'created',
            'created_utc',
            'permalink',
            'score',
            'body',)
        for comment in reddit.redditor(cfg['username']).comments.new(limit=5):
            comment_dict = vars(comment)
            sub_dict = OrderedDict()
            for field in fields:
                sub_dict[field] = comment_dict[field]
            sub_dict['permalink'] = 'https://www.reddit.com' + sub_dict['permalink']
            # Convert to readable timestamp
            sub_dict['local_time'] = time.strftime('%Y-%m-%d %I:%M:%S %p EST', time.localtime(sub_dict['created_utc']))
            json_string = json.dumps(sub_dict, indent=4) + '\n'
            file.write(json_string)
        file.close()
    except OSError:
        print("Unable to create file \"%s\". Please check that the file path is valid.")


def overwrite_comments(reddit):
    logger.info("Overwriting all comments...")


def main():
    reddit = connect()
    logger.info("Logged in as user \"u/%s\"...", cfg['username'])
    export_comments(reddit)
    overwrite_comments(reddit)


if __name__ == '__main__':
    main()
