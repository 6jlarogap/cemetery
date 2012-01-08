#! /bin/bash

PACKAGES="	acpid
		git-core
		htop
		links
		mc
		nginx
		openssh-client
		openssh-server
		patch
		postgresql-8.4
		python-cheetah
		python-egenix-mxdatetime
		python-egenix-mxtools
		python-flup
		python-newt
		python-psycopg2
		python-webpy
		screen
		ssl-cert
		tcpd
		traceroute
		unrar
		unzip
		vim
		vim-runtime
		samba
		"
for i in $PACKAGES; do
 apt-get install -y $i
done
