#!/bin/bash

${HOME}/.screenlayout/main.sh &
sxhkd -c ~/.config/sxhkd/qtilerc &
picom &
killall redshift -q
redshift &
python ${HOME}/.config/polybar/polybar_wallpaper.py &
${HOME}/.config/polybar/launch.sh &