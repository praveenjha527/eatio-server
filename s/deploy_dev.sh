PROJECT_PATH='/home/sayonetech/webapps/eatio'
PROJECT_DIR='eatio/eatio_web'
PROJECT_DIR_PATH=${PROJECT_PATH}/${PROJECT_DIR}

cd ${PROJECT_DIR_PATH}
git checkout develop
git pull origin develop

cd ${PROJECT_PATH}/virtual && source bin/activate
cd ${PROJECT_DIR_PATH}

pip install -r requirements.txt

python manage.py migrate  --noinput
python manage.py collectstatic  --noinput

${PROJECT_PATH}/apache2/bin/restart
