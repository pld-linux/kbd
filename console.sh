
case $TERM in
 linux)
 	if [ -f /etc/sysconfig/console ]; then
		. /etc/sysconfig/console
	
		if [ "$CONSOLEMAP" != "" ]; then
			# Switch the G0 charset map from the default ISO-8859-1
			# to the user-defined map (loaded with consolefonts)
			if [ -w /proc/$$/fd/0 ]; then
				echo -n -e '\033(K' > /proc/$$/fd/0
			else
				echo -n -e '\033(K' > /dev/tty
			fi
		fi
		
	fi
	;;
esac
