PROJECT_PATH='/home/sayonetech/webapps/eatio_production'
PROJECT_DIR='eatio/eatio_web'
PROJECT_DIR_PATH=${PROJECT_PATH}/${PROJECT_DIR}

cd ${PROJECT_DIR_PATH}
git checkout master
git pull origin master

cd ${PROJECT_PATH}/virtual && source bin/activate
cd ${PROJECT_DIR_PATH}

pip install -r requirements.txt

python manage_prod.py migrate  --noinput
python manage_prod.py collectstatic  --noinput

${PROJECT_PATH}/apache2/bin/restart
