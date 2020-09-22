#!/bin/sh
cd $(dirname "$0")/target
cp mydb.db.orig /rw/mydb.db
python manage.py runserver 0.0.0.0:$1
