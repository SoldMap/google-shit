import pygsheets

# Initialize and authorize connection to spreadsheet
# return a worksheet object
# the problem is whe nI call it from several consequent 
# modules I will likely be losing unsaved info. So, 
# just remember that when passing between modules info is not saved 

def initialize_connection():
    connect = pygsheets.authorize(service_file="/home/misha/Playground/Python/google-shit/service_account_credentials.json")

    spsh = connect.open_by_url("https://docs.google.com/spreadsheets/d/iii111/edit#gid=0")
        
    return spsh[0]
