# stock-finder
Searches the web for PS5, RTX 3000 series, and more(soon™)!
When stock is found, a link opens a new tab inside your default browser. Can also send emails and sms notifications.

# Options
To select what you want the program to search for, open the stockfinder.ini file. Everything is toggled on by default. 0 = disable, 1 = enable.
Stockfinder.ini will be generated in the same directory as stockfinder.py. Default search time is 1 minute. To change, edit stockfinder.py in a text editor and change MINUTES from 1.0 to a time you prefer.

# Emails and SMS alerts
SMS functionality is afforded by twilio: https://www.twilio.com/ Sign up for a free trial and plug in your api credentials inside stockfinder.ini.
To have emails and text message alerts sent, fill in your credentials inside the stockfinder.ini file.

Only gmail accounts supported at this time. In order for the script to send emails, you will have to toggle "allow less secure apps" on in your google account (use a dummy email): https://myaccount.google.com/lesssecureapps

# Other notes
You may have to install the twilio module using pip. To do so, just run "pip install twilio".
