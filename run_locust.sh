#!/bin/bash

if [ -z "$URL" ]; then
    URL="$1"
fi
echo "URL='$URL'"
if [ -z "$URL" ]; then
    echo "please specify a URL"
    exit 1
fi

# if it's already on path, guess we should use that
if [ -n "$(command -v locust)" ]; then
    LOCUST=locust

# otherwise look for ./locust_env
elif [ -d locust_env ] && [ -x "locust_env/bin/locust" ]; then
    LOCUST=locust_env/bin/locust

else
    echo "Can't find a locust to use"
    exit 1
fi

$LOCUST --version

LOGLEVEL=INFO
echo "Starting locust: $LOCUST (log level $LOGLEVEL)"
$LOCUST -f ./code/tile_tester.py --loglevel="$LOGLEVEL" --host="$URL"

# Crude example of how to use multiple cores against chopper
# $LOCUST -f ./code/tile_tester.py --master --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
# $LOCUST -f ./code/tile_tester.py --slave --loglevel="$LOGLEVEL" --host="$URL" &
