#!/usr/bin/env bash
source constants
#pg_dump -U postgres cemetery | gzip > /var/cemetery/dumps/"`eval date +%Y%m%d`".gz
pg_dump -U postgres cemetery | gzip > $db_dumps_dir/"`eval date +%Y%m%d`".gz
#rsync -av --delete /var/cemetery/media/ofiles /var/cemetery/dumps/
rsync -av --delete /home/django/projects/cemetery/media/ofiles /var/cemetery/dumps/
