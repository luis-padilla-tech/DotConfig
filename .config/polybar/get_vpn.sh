get_tunnel_command="ip addr | awk '/tun96:/ {print}'"
output=$(eval "$get_tunnel_command")

if [ "$output" == "" ];
then
	echo ''
else
	echo ''
fi