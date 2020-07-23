#!/bin/bash

APP_HOME=$(dirname $(realpath $0))
. $APP_HOME/conf/env.sh
APP_VAR=$APP_HOME/var
APP_TMP=$APP_VAR/tmp
APP_LOG=$APP_VAR/log
APP_LOG_FILE=$APP_LOG/messages.log

# Check if dirs exist
if [ ! -d $APP_VAR ]; then
	echo "[ERROR] $APP_VAR does not exist." 
	exit 1
fi
if [ -f $APP_VAR/pid ]; then
	PID=$(cat $APP_VAR/pid)
	echo "[INFO] Stopping gunicorn process $PID" >> $APP_LOG_FILE
	kill $PID
	exit 0
else 
	echo "[ERROR] $APP_VAR/pid does not exist."
	exit 1
fi
