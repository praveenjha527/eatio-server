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
supervisorctl restart celeryd (restart)
celery worker --app=eatio_web -l info (running celery)
ps aux | grep celery (to see the celery process)

http://thomassileo.com/blog/2012/08/20/how-to-keep-celery-running-with-supervisor/




