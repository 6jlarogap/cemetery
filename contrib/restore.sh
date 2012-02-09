#!/bin/sh

dropdb -U postgres cemetery
echo 'Cleaned'

createdb -U postgres cemetery
echo 'Created'

cat $1 | psql -U postgres cemetery
echo 'Finished'
