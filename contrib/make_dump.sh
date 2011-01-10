#!/bin/sh
pg_dump -U postgres youmemory | gzip > /home/tier/tmp/dumps/"`eval date +%Y%m%d`".gz
