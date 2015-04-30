# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': '/home/user/projects/eatio/eatio_web/eatio_web/db_files/my_local.cnf',
#             'init_command': 'SET storage_engine=INNODB',
#         },
#     }
# }


DATABASES = {
   'default': {
   'ENGINE': 'django.db.backends.mysql',
   'NAME':'eatio',
   'USER': 'sayone',
   'PASSWORD': 'password',
   'HOST':'',
   'PORT':'',
    },
}
