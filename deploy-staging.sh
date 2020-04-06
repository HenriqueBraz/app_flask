#!/bin/bash

cd /home/sites-python/ && (
        chown novorumo.areadetestes.com.br:www-data novorumo.areadetestes.com.br
)

cd /home/sites-python/novorumo.areadetestes.com.br && (
        chown -R novorumo.areadetestes.com.br:www-data LICENSE Procfile __pycache__ app config.json project.ini requirements.txt novorumo.sock;
        chown -R root. .git .gitignore .gitlab-ci.yml project.ini
        chmod a+r project.ini
        chmod 700 $0
)