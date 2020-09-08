# archive-reddit-comments
 
* This Python script exports all of your Reddit account's comments as a JSON file, overwrites them with `[deleted]`, then deletes them.
* The overwrite step is needed because the body of deleted comments can still be viewed via Reddit API calls.

## Usage
* You must first register your account for a script application on Reddit. Follow the instructions here: http://praw.readthedocs.io/en/latest/getting_started/authentication.html
* Then, enter your credentials into [config.yaml](config.yaml).
* `python3 archive_comments.py` exports your comments to `comments.json` in the current directory, then overwrites and deletes.
  * You can just run `make` to execute this.
* `python3 archive_comments.py --path your_file_path_here` exports your comments to `comments.json` in the path that you specify, then overwrites and deletes.
* It may take a couple minutes for the script to delete all the comments; the script is multithreaded, but Reddit rate-limits your API calls.
