# ZipCode
A Web App for searching through Indian Zipcodes 

##Installation

Do a Fabric Deployment with the script in /deployment Folder 

 >> fab production deploy 
 
 PS : Change the settings.py file database user/password if required 
 
 ##Load Data To Redis
 After Installation is complete you need to load all the data from csv to redis once 

 >> Python manage.py databuilder 
 
 This will call the django command zipapp and will load the csv data to redis.
 
 
##Celery And Worker Configuration 
 
 Run Celery by demon as 
 
 >> celery -A zipapp --concurrency=10 worker -l debug
 
 
##Setup Gunicorn 

>> gunicorn --workers=2 zipcode.wsgi

You can also run it with supervisord


##Demo URL 

http://54.69.200.1 

