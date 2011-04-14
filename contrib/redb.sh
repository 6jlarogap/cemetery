#!/bin/sh
#User for django
dropdb -U postgres cemetery
createdb -U postgres cemetery
#cat cemetery.sql | psql -U postgres cemetery
