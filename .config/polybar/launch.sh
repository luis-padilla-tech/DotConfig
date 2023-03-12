killall polybar -q

if type "xrandr"; then
  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m polybar horizontal --reload &
  done
else
  polybar horizontal --reload &
fi