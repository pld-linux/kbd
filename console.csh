
if ( $TERM == "linux" ) then
	if ( -f /etc/sysconfig/console ) then
		if ( { sh -c '. /etc/sysconfig/console ; [ -n "$CONSOLEMAP" ] || exit 1' } ) then
			set previous_echo_style=$echo_style
			set echo_style=both
			# Switch the G0 charset map from the default ISO-8859-1
			# to the user-defined map (loaded with consolefonts)
			if ( -w /proc/$$/fd/0 ) then
				echo -n '\033(K' > /proc/$$/fd/0
			else
				echo -n '\033(K' > /dev/tty
			endif
			set echo_style=$previous_echo_style
			unset previous_echo_style
		endif
		
	endif
endif
