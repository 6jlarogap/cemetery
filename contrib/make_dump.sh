#!/usr/bin/env bash
source constants
pg_dump -U postgres cemetry | gzip > $db_dumps_dir/"`eval date +%Y%m%d`".gz
