#!/usr/bin/env bash
source constants
pg_dump -U postgres cemetery | gzip > $db_dumps_dir/"`eval date +%Y%m%d`".gz
rsync -av /home/django/projects/cemetery/media/ofiles /var/cemetery/dumps/
