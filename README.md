# eatio

###How to create apply migrations easily on AWS instance:
1. `chmod +x applymigrate` to make this applymigrate file executable

2. `./applymigrate` . This will syncdb, migrate in order of dependencies. 

###How to Start wsgi :

1. Activate virtual enviornment

2. run uwsgi --ini uwsgi.ini 

###How to Stop wsgi :

sudo killall -s INT /home/ubuntu/eatio_env/bin/uwsgi

###Celery 
1. supervisorctl restart celeryd (restart)
2. celery worker --app=eatio_web -l info (running celery)
3. ps aux | grep celery (to see the celery process)

##Clear Table
drop schema public cascade;
create schema public;

Then apply migrations from the scratch

http://thomassileo.com/blog/2012/08/20/how-to-keep-celery-running-with-supervisor/

http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html



