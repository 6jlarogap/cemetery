#!/bin/sh
scp /var/cemetery/outbox/*.json soul@192.168.0.5:/var/cemetery/inbox/
&&
rm -rf /var/cemetery/outbox/*.json
