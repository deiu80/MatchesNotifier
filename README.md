# MatchesNotifier
IT REQUIRES THE FOLLOWING PACKAGES INSTALLS:

pip install bs4
pip install mysql.connector
pip install requests

A python script that sends an email with today's matches and also stores, updates and deletes matches from mysql database.
  U should first create the database, then the table using createtable.py, and edit the email variables from EmailSending.py to your preference (make sure you change the setting " Allow less secure apps to ON" on the sender gmail account).
  Put the files in the same folder and run the EmailSending.py. This will also create 2 text report files: One with the email content and one with database updates and delets performed.
  More teams can be added by putting their skysports fixtures link in the url_dict.
  Obviously, it is merely a simple , fun script which means it is not secure. I highly reccommend creating a gmail account to test this out.
  IT ONLY WORKS FOR SKYSPORTS WEBSITE, BECAUSE THAT'S HOW I DESIGNED IT
