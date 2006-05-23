[ -f /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n

tty -s
if [ $? -eq 0 ]; then
 case $TERM in
  linux)
 	if [ -f /etc/sysconfig/console ]; then
		. /etc/sysconfig/console

		case "$LANG" in
			*.utf8|*.UTF-8)
				[ -x /bin/unicode_start ] && /sbin/consoletype fg && /bin/unicode_start
			;;
		esac

		if [ "$CONSOLEMAP" != "" ]; then
			# Switch the G0 charset map from the default ISO-8859-1
			# to the user-defined map (loaded with consolefonts)
			if [ -w /proc/$$/fd/0 -a -t 0 ]; then
				echo -n -e '\033(K' > /proc/$$/fd/0
			else
				echo -n -e '\033(K' > /dev/tty
			fi
		fi
		
	fi
	;;
 esac
fi
