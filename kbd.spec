# TODO
# - probably it doesn't make sense to package ppc keymaps on x86 and vice versa
Summary:	Linux console utilities
Summary(ko.UTF-8):	콘솔을 설정하는 도구 (글쇠판, 가상 터미널, 그 밖에)
Summary(pl.UTF-8):	Narzędzia do obsługi konsoli
Name:		kbd
Version:	1.15.3
Release:	1
License:	GPL v2+
Group:		Applications/Console
Source0:	ftp://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.gz
# Source0-md5:	8143e179a0f3c25646ce5085e8777200
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	93c72a27e4fdeba23cb62d62343e9483
Source4:	lat2u-16.psf.gz
# Source4-md5:	dc90a9bcff858175beea32a9b3bebb33
Source5:	lat2u.sfm.gz
# Source5-md5:	8ac4abc169fa1236fc3e64163c043113
Source6:	console.sh
Source7:	console.csh
Source8:	%{name}-pl1.kmap
Source9:	%{name}-mac-pl.kmap
Source10:	%{name}-pl3.map
Source11:	%{name}-pl4.map
Patch0:		%{name}-unicode_start.patch
Patch1:		%{name}-ngettext.patch
Patch2:		%{name}-tty-detect.patch
Patch3:		%{name}-defkeymap.patch
Patch4:		%{name}-po.patch
URL:		http://www.win.tue.nl/~aeb/linux/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.14.1
Requires(post,preun):	/sbin/chkconfig
Requires:	open
Requires:	rc-scripts >= 0.4.3.0
Requires:	sed
Requires:	util-linux
Provides:	console-data
Provides:	console-tools
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--datadir=%{_ldatadir} \
	--localedir=%{_datadir}/locale \
	--enable-nls
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/etc/{profile.d,rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# some binaries are needed in /bin but rest is not
for f in setfont dumpkeys kbd_mode unicode_start unicode_stop; do
	mv $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT/bin
done

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
%ifarch sparc sparc64
sed -i -e 's/KEYTABLE=pl2/KEYTABLE=sunkeymap/' $RPM_BUILD_ROOT/etc/sysconfig/console
%endif

cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_ldatadir}/consolefonts/lat2u-16.psfu.gz
gunzip -c %{SOURCE5} > $RPM_BUILD_ROOT%{_ldatadir}/unimaps/lat2u.uni

gzip -c %{SOURCE8} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl1.map.gz
gzip -c %{SOURCE9} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/mac/all/mac-pl.map.gz
gzip -c %{SOURCE10} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl3.map.gz
gzip -c %{SOURCE11} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl4.map.gz

cp -a %{SOURCE6} $RPM_BUILD_ROOT/etc/profile.d
cp -a %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%{__rm} doc/{*,*/*}.sgml

# Greek is el, not gr
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/gr
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{README.kbd-non-english-man-pages,kbd-keypaps_instead_keytables.patch}*

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
%doc AUTHORS COPYING ChangeLog README doc/*.txt
%attr(754,root,root) /etc/rc.d/init.d/console
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/console
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
%attr(755,root,root) %{_bindir}/resizecons
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
%{_mandir}/man8/resizecons.8*
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
