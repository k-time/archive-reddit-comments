import argparse
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

def get_file_location():
    # Command-line options parser
    parser = argparse.ArgumentParser(description='Reddit bot that searches and posts MMA scorecards.')
    parser.add_argument('-l', '--location', dest='location', help='Set the exp.')
    args = parser.parse_args()

    if args.location is not None:
        location = args.location
        if not location.endswith("/") and not location.endswith("\\"):
            if "\\" in location:
                location += "\\"
            else:
                location += "/"
        return location + cfg['default_file_location']
    else:
        return cfg['default_file_location']


def main():
    reddit = connect()
    file_location = get_file_location()
    logger.info("Deleting comments for user \"u/%s\" and saving to file \"%s\"...", cfg['username'], file_location)

if __name__ == '__main__':
    main()
