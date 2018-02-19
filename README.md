# delete-reddit-comments
 
* This Python command-line app exports all of your Reddit account's comments as a JSON file.
* It then overwrites all of the comments with "[deleted]".

## Background
* When you delete a Reddit comment, it just changes a flag in Reddit's comment database. The comment text will still exist.
* If you edit the comment, it will overwrite the comment value in the database. Thus, to actually delete all of your Reddit comments, you must overwrite them.
* Reddit says they don't store the edit history of a post—hopefully this is the truth.

## Usage
* You must first register your account for a script application on Reddit. Follow the instructions here: http://praw.readthedocs.io/en/latest/getting_started/authentication.html
