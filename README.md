# stock-finder
Searches the web for PS5, RTX 3000 series, and more(soon™)!
When stock is found, a link opens a new tab inside your default browser.

# Options
To select what you want the program to search for, open the stockfinder.ini file. Everything is toggled on by default. 0 = disable, 1 = enable.
Stockfinder.ini will be generated in the same directory as stockfinder.py.
Default search time is 30 seconds. To change, edit stockfinder.py in a text editor and change MINUTES from 0.5 to a time you prefer.

Example: ps5 = 0 # don't search for ps5

# Emails and SMS alerts
SMS functionality is afforded by twilio: https://www.twilio.com/ Sign up for a free trial and plug in your api credentials inside Alert.py.
To have emails and text message alerts sent, fill in your credentials inside the Alert.py file. Highly recommended to use a dummy email. This will soon be deprecated.

# Other notes
You may have to install the twilio module using pip. To do so, just run "pip install twilio".
