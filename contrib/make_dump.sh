#!/bin/sh
pg_dump -U postgres cemetry | gzip > /home/tier/tmp/dumps/"`eval date +%Y%m%d`".gz
