# NOTE: kbd's vlock is a fork of vlock v1.x
#       comparing with vlock v2.x it has NLS, but no plugins support
# TODO:
# - pam file for vlock
# - probably it doesn't make sense to package ppc keymaps on x86 and vice versa
#
# Conditional build:
%bcond_without	vlock	# don't build vlock
#
Summary:	Linux console utilities
Summary(ko.UTF-8):	콘솔을 설정하는 도구 (글쇠판, 가상 터미널, 그 밖에)
Summary(pl.UTF-8):	Narzędzia do obsługi konsoli
Name:		kbd
Version:	2.0.0
Release:	1
License:	GPL v2+
Group:		Applications/Console
Source0:	ftp://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.gz
# Source0-md5:	5ba259a0b2464196f6488a72070a3d60
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	93c72a27e4fdeba23cb62d62343e9483
Source4:	lat2u-16.psf.gz
# Source4-md5:	dc90a9bcff858175beea32a9b3bebb33
Source5:	lat2u.sfm.gz
# Source5-md5:	8ac4abc169fa1236fc3e64163c043113
Source51:	http://pkgs.fedoraproject.org/repo/pkgs/kbd/%{name}-latsun-fonts.tar.bz2/050e1e454e9c01e22f198303d649efb8/kbd-latsun-fonts.tar.bz2
# Source51-md5:	050e1e454e9c01e22f198303d649efb8
Source52:	http://pkgs.fedoraproject.org/repo/pkgs/kbd/%{name}-latarcyrheb-16-fixed.tar.bz2/cb1e2d5ba5d4cb8b0a27367029d36a56/kbd-latarcyrheb-16-fixed.tar.bz2
# Source52-md5:	cb1e2d5ba5d4cb8b0a27367029d36a56
Source6:	console.sh
Source7:	console.csh
Source8:	%{name}-pl1.kmap
Source9:	%{name}-mac-pl.kmap
Source10:	%{name}-pl3.map
Source11:	%{name}-pl4.map
Source12:	console.upstart
Patch0:		%{name}-unicode_start.patch
Patch1:		%{name}-ngettext.patch
Patch2:		%{name}-tty-detect.patch
Patch3:		%{name}-pl.po-update.patch
URL:		http://www.win.tue.nl/~aeb/linux/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
#BuildRequires:	check >= 0.9.4
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	libtool >= 2:2
%{?with_vlock:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	open
Requires:	rc-scripts >= 0.4.3.0
Requires:	sed
Requires:	util-linux
Obsoletes:	console-data
Obsoletes:	console-tools
Obsoletes:	console-tools-devel
Obsoletes:	console-tools-static
Conflicts:	man-pages < 1.43-5
Conflicts:	util-linux < 2.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ldatadir	/lib/%{name}

%description
This package contains utilities to load console fonts and keyboard
maps. It also includes a number of different fonts and keyboard maps.

%description -l pl.UTF-8
Pakiet zawiera narzędzia do ładowania fontów konsolowych oraz map
klawiatury. Dodatkowo dołączono znaczną liczbę różnych fontów i map.

%package vlock
Summary:	Utility to lock one or more virtual consoles
Summary(pl.UTF-8):	Narzędzie do blokowania jednej lub wielu konsol wirtualnych
Group:		Applications/Console
Requires:	%{name} = %{version}-%{release}

%description vlock
Utility to lock one or more virtual consoles.

%description vlock -l pl.UTF-8
Narzędzie do blokowania jednej lub wielu konsol wirtualnych.

%package libs
Summary:	libkeymap - library to manage the Linux keymaps
Summary(pl.UTF-8):	libkeymap - biblioteka do zarządzania linuksowymi przypisaniami klawiszy
Group:		Libraries

%description libs
libkeymap - library to manage the Linux keymaps.

%description libs -l pl.UTF-8
libkeymap - biblioteka do zarządzania linuksowymi przypisaniami
klawiszy.

%package devel
Summary:	Header files for libkeymap library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libkeymap
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for libkeymap library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libkeymap.

%package static
Summary:	Static libkeymap library
Summary(pl.UTF-8):	Statyczna biblioteka libkeymap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libkeymap library.

%description static -l pl.UTF-8
Statyczna biblioteka libkeymap.

%prep
%setup -q -a51 -a52
%patch3 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--datadir=%{_ldatadir} \
	--localedir=%{_datadir}/locale \
	--enable-libkeymap \
	--enable-nls \
	--disable-silent-rules \
	%{!?with_vlock:--disable-vlock}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/etc/{profile.d,rc.d/init.d,sysconfig,init}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# some binaries are needed in /bin but the rest is not
for f in setfont dumpkeys kbd_mode unicode_start unicode_stop; do
	mv $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT/bin
done

# move library to /lib* for utils in /bin
install -d $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libkeymap.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf $(basename $RPM_BUILD_ROOT/%{_lib}/libkeymap.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libkeymap.so
# no external dependencies; also .pc file exists
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libkeymap.la

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
cp -p %{SOURCE12} $RPM_BUILD_ROOT/etc/init/console.conf
%ifarch sparc sparc64
%{__sed} -i -e 's/KEYTABLE=pl2/KEYTABLE=sunkeymap/' $RPM_BUILD_ROOT/etc/sysconfig/console
%endif

cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_ldatadir}/consolefonts/lat2u-16.psfu.gz
gunzip -c %{SOURCE5} > $RPM_BUILD_ROOT%{_ldatadir}/unimaps/lat2u.uni

gzip -c %{SOURCE8} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl1.map.gz
gzip -c %{SOURCE9} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/mac/all/mac-pl.map.gz
gzip -c %{SOURCE10} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl3.map.gz
gzip -c %{SOURCE11} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl4.map.gz

cp -p %{SOURCE6} $RPM_BUILD_ROOT/etc/profile.d
cp -p %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

# Greek is el, not gr
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/gr
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{README.kbd-non-english-man-pages,kbd-keypaps_instead_keytables.patch}*

# doxygen docs
%{__rm} -rf docs-doxy
%{__mv} $RPM_BUILD_ROOT%{_docdir}/kbd/html docs-doxy

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add console

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains copyright summary, not GPL text
%doc AUTHORS COPYING CREDITS ChangeLog README docs/doc/kbd.FAQ.txt
%attr(754,root,root) /etc/rc.d/init.d/console
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/console
%config(noreplace) %verify(not md5 mtime size) /etc/init/console.conf
%attr(755,root,root) /etc/profile.d/console.csh
%attr(755,root,root) /etc/profile.d/console.sh

%attr(755,root,root) /bin/dumpkeys
%attr(755,root,root) /bin/kbd_mode
%attr(755,root,root) /bin/setfont
%attr(755,root,root) /bin/unicode_start
%attr(755,root,root) /bin/unicode_stop
%attr(755,root,root) %{_bindir}/chvt
%attr(755,root,root) %{_bindir}/deallocvt
%attr(755,root,root) %{_bindir}/fgconsole
%attr(755,root,root) %{_bindir}/getkeycodes
%attr(755,root,root) %{_bindir}/kbdinfo
%attr(755,root,root) %{_bindir}/kbdrate
%attr(755,root,root) %{_bindir}/loadkeys
%attr(755,root,root) %{_bindir}/loadunimap
%attr(755,root,root) %{_bindir}/mapscrn
%attr(755,root,root) %{_bindir}/openvt
%attr(755,root,root) %{_bindir}/psfaddtable
%attr(755,root,root) %{_bindir}/psfgettable
%attr(755,root,root) %{_bindir}/psfstriptable
%attr(755,root,root) %{_bindir}/psfxtable
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_bindir}/resizecons
%endif
%attr(755,root,root) %{_bindir}/setkeycodes
%attr(755,root,root) %{_bindir}/setleds
%attr(755,root,root) %{_bindir}/setmetamode
%attr(755,root,root) %{_bindir}/setvtrgb
%attr(755,root,root) %{_bindir}/showconsolefont
%attr(755,root,root) %{_bindir}/showkey
%dir %{_ldatadir}
%{_ldatadir}/consolefonts
%{_ldatadir}/consoletrans
%{_ldatadir}/keymaps
%{_ldatadir}/unimaps

%{_mandir}/man1/chvt.1*
%{_mandir}/man1/deallocvt.1*
%{_mandir}/man1/dumpkeys.1*
%{_mandir}/man1/fgconsole.1*
%{_mandir}/man1/kbd_mode.1*
%{_mandir}/man1/loadkeys.1*
%{_mandir}/man1/openvt.1*
%{_mandir}/man1/psfaddtable.1*
%{_mandir}/man1/psfgettable.1*
%{_mandir}/man1/psfstriptable.1*
%{_mandir}/man1/psfxtable.1*
%{_mandir}/man1/setleds.1*
%{_mandir}/man1/setmetamode.1*
%{_mandir}/man1/showkey.1*
%{_mandir}/man1/unicode_start.1*
%{_mandir}/man1/unicode_stop.1*
%{_mandir}/man5/keymaps.5*
%{_mandir}/man8/getkeycodes.8*
%{_mandir}/man8/kbdrate.8*
%{_mandir}/man8/loadunimap.8*
%{_mandir}/man8/mapscrn.8*
%ifarch %{ix86} %{x8664}
%{_mandir}/man8/resizecons.8*
%endif
%{_mandir}/man8/setfont.8*
%{_mandir}/man8/setkeycodes.8*
%{_mandir}/man8/setvtrgb.8*
%{_mandir}/man8/showconsolefont.8*
%lang(es) %{_mandir}/es/man[158]/*
%lang(fi) %{_mandir}/fi/man[158]/*
%lang(fr) %{_mandir}/fr/man[158]/*
%lang(hu) %{_mandir}/hu/man[158]/*
%lang(ko) %{_mandir}/ko/man[158]/*
%lang(pl) %{_mandir}/pl/man[158]/*

%if %{with vlock}
%files vlock
%defattr(644,root,root,755)
%doc src/vlock/README.vlock
%attr(755,root,root) %{_bindir}/vlock
%{_mandir}/man1/vlock.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libkeymap.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libkeymap.so.0

%files devel
%defattr(644,root,root,755)
%doc docs-doxy/*
%attr(755,root,root) %{_libdir}/libkeymap.so
%{_includedir}/keymap
%{_includedir}/keymap.h
%{_pkgconfigdir}/libkeymap.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libkeymap.a
