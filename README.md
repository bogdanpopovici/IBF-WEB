I've been found

Prerequisites:

Python 2.7 -> https://www.python.org/downloads/release/python-279/
pip -> https://pypi.python.org/pypi/pip
EB Command Line Interface (EB CLI) -> http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html

Get code:

Open a commandline prompt and type 'git clone https://github.com/bogdanpopovici/IBF-WEB.git'; 
   or
On your github account, navigation to the IBF-WEB repo and download the zip, then extract it on your machine;

Live Deployment (Windows) 

Open a commandline prompt 
Navigate to IBFWeb\ and type 'eb deploy' 
Open a browser and go to 'http://ivebeenfound-dev2.elasticbeanstalk.com' to see if the application went live. 
If you encounter difficulties in accessing the website, check app's status at https://us-west-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-west-2#/environment/dashboard?applicationName=Ivebeenfound&environmentId=e-pepxdsx58p

Local Testing (Windows) 

Open a commandline prompt 
Navigate to IBFWeb\ibfEnv\Scripts 
Type 'activate' 
Go back to the root folder and type 'pip install -r requirements' (this is required only the first time you run the application locally) 
Type 'python manage.py runserver'. At this point, you should see the server starting with a proper message 
Open a browser and go to 'localhost:8000'. This is the url for testing your local version of the app

Administration panel

Go to http://ivebeenfound-dev2.elasticbeanstalk.com/admin/ 
Login with your admin credentials 
Each section represents a table in the database. Open a link to see its entries. 
As an admin, you can create, delete or modify objects of the database including user accounts. 
It is worth mentioning that when you delete an object, all the other objects related to it will be deleted recursively (i.e. when yu delete an user you will also delete the items he/she uploaded, their related images etc.)
