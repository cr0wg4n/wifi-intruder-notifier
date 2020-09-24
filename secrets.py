# Your devices' whitelist, key 'mac' is mandatory in every dictionary 

WHITE_LIST = [
    {
        'mac': 'xx:xx:xx:xx:xx:xx',
        'owner': 'Home',
        'device_name': 'Home Router'
    },
    {
        'mac': 'xx:xx:xx:xx:xx:xx',
        'owner': 'James',
        'device_name': 'James PC'
    }
]

# Twilio page: https://www.twilio.com/messaging

TWILIO_ACCOUNT_SID = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
TWILIO_AUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
TWILIO_PHONE_NUMBER = '+1662123213' # twilio's number 
YOUR_NUMBER = '+59174121222' # region code + your number
TIME_MIN = 30 # the scripts runs every X minutes