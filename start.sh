
#!/bin/bash

APP_HOME=$(dirname $(realpath $0))
. $APP_HOME/conf/env.sh
APP_VAR=$APP_HOME/var
APP_TMP=$APP_VAR/tmp
APP_LOG=$APP_VAR/log
APP_LOG_FILE=$APP_LOG/messages.log
export prometheus_multiproc_dir=$APP_TMP

# Check if dirs exist
if [ ! -d $APP_VAR ]; then
	mkdir -p $APP_VAR
fi
if [ ! -d $APP_TMP ]; then
	mkdir -p $APP_TMP
else # ensure it is empty
	rm -rf $APP_TMP/*
fi
if [ ! -d $APP_LOG ]; then
	mkdir -p $APP_LOG
fi

# Start the app with gunicorn

cd $APP_HOME
$GUNICORN -p $APP_VAR/pid -c gunicorn_conf.py -w $GUNICORN_WORKERS -b $GUNICORN_HOST:$GUNICORN_PORT $GUNICORN_OPTS main:app  &>> $APP_LOG_FILE &
