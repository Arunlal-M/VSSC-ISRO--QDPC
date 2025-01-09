 set LnD_PATH=%~dp0
cmd /k "cd /d %LnD_PATH%env/Scripts & activate & cd /d %LnD_PATH% & python manage.py runserver 8010"