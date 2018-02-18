import argparse
import json
import logging
import praw
import sys
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

def save_and_delete_comments(file_path):
    try:
        file = open(file_path, 'w+')
    except OSError:
        print("Unable to create file \"%s\". Please check that the file path is valid.")

def main():
    reddit = connect()
    file_path = get_file_path()
    logger.info("Deleting comments for user \"u/%s\" and saving to file \"%s\"...", cfg['username'], file_path)
    save_and_delete_comments(file_path)

if __name__ == '__main__':
    main()
