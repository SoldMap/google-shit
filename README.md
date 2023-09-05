# google-shit

The goal of having this autoamtion:
--
When the new machine is deployed, we need to get the board details, ip address and its physical location get tracked \n

This is the structure of the spreadsheet:\n
![spsh](https://github.com/SoldMap/google-shit/assets/85728542/ea8c2cfb-e39f-4072-b762-a7f652bfaa61)

To make this work, I need 2 things - establish connection from the Python app to the Spreadsheet, and pull the details 
from every machine to that spreadsheet.
I use Google Workspace service account credentials for authentiacation and authorization \n
All the interaction with google API is done with the **pygsheets** library \n\n

This script maintains the order of the list, when machine needs to get into deployed section.\n
For that reason there are several argument parsers - build, rebuild, deploy, and move... \n
So, this script handles the whole lifecycle of the machine, making sure all the inforamation is up to date and reliable


