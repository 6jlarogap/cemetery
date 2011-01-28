#!/bin/sh
source constants
scp $outbox_dir/*.json soul@$server_addr:$inbox_dir/
rm -rf $outbox_dir/*.json
