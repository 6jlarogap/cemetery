# /etc/skel/.bash_profile

# This file is sourced by bash for login shells.  The following line
# runs your .bashrc and is recommended by the bash info pages.
#[[ -f ~/.bashrc ]] && . ~/.bashrc
#pgrep X >/dev/null || exec startx 

#if [ -f ~/.bashrc ]; then
#   source ~/.bashrc
#   fi

# X server startup
if [ -z "$DISPLAY" ] && [ $(tty) == /dev/tty1 ] && [[ ${EUID} != 0 ]]; then
    startx > /dev/null
fi
