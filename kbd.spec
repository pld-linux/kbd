Summary:	Linux console utilities
Summary(ko):	ÄÜ¼ÖÀ» ¼³Á¤ÇÏ´Â µµ±¸ (±Û¼èÆÇ, °¡»ó ÅÍ¹Ì³Î, ±× ¹Û¿¡)
Summary(pl):	Narzêdzia do obs³ugi konsoli
Name:		kbd
Version:	1.12
Release:	4
License:	GPL
Group:		Applications/Console
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/kbd/%{name}-%{version}.tar.gz
# Source0-md5:	7892c7010512a9bc6697a295c921da25
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
Source8:	console-man-pages.tar.bz2
# Source8-md5:	3790029011f9f2e299ea4e56df0fa0f9
Source9:	%{name}-pl1.kmap
Source10:	%{name}-mac-pl.kmap
Source11:	%{name}-pl3.map
Source12:	%{name}-pl4.map
Patch0:		%{name}-pl.po-update.patch
Patch1:		%{name}-missing-nls.patch
Patch2:		%{name}-install.patch
Patch3:		%{name}-sparc.patch
Patch4:		%{name}-compose.patch
Patch5:		%{name}-compat-suffixes.patch
Patch6:		%{name}-unicode_start.patch
Patch7:		%{name}-posixsh.patch
Patch8:		%{name}-gcc33.patch
Patch9:		%{name}-pl.patch
Patch10:	%{name}-pl2.patch
Patch11:	%{name}-terminal.patch
URL:		http://www.win.tue.nl/~aeb/linux/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	sed
Requires:	open
Requires:	util-linux
Provides:	console-data
Provides:	console-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	util-linux < 2.11
Conflicts:	man-pages < 1.43-5
Obsoletes:	console-data
Obsoletes:	console-tools
Obsoletes:	console-tools-devel
Obsoletes:	console-tools-static

%define	_ldatadir	/%{_lib}/%{name}

%description
This package contains utilities to load console fonts and keyboard
maps. It also includes a number of different fonts and keyboard maps.

%description -l pl
Pakiet zawiera narzêdzia do ³adowania fontów konsolowych oraz map
klawiatury. Dodaktowo do³±czono znaczn± liczbê ró¿nych fontów i map.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
./configure \
	--prefix=/ \
	--datadir=%{_ldatadir} \
	--mandir=%{_mandir}
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir},/etc/{profile.d,rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# some binaries are needed in /bin but rest is not
mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}
for f in setfont dumpkeys kbd_mode unicode_start unicode_stop; do
  mv $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT/bin
done

mv $RPM_BUILD_ROOT/share/locale $RPM_BUILD_ROOT%{_datadir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
%ifarch sparc sparc64
sed 's/KEYTABLE=pl2/KEYTABLE=sunkeymap/' %{SOURCE2} > $RPM_BUILD_ROOT/etc/sysconfig/console
%else
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
%endif

install %{SOURCE4} $RPM_BUILD_ROOT%{_ldatadir}/consolefonts/lat2u-16.psfu.gz
gunzip -c %{SOURCE5} >$RPM_BUILD_ROOT%{_ldatadir}/unimaps/lat2u.uni

gzip -c %{SOURCE9} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl1.map.gz
gzip -c %{SOURCE10} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/mac/all/mac-pl.map.gz
gzip -c %{SOURCE11} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl3.map.gz
gzip -c %{SOURCE12} > $RPM_BUILD_ROOT%{_ldatadir}/keymaps/i386/qwerty/pl4.map.gz

install %{SOURCE6} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

bzip2 -dc %{SOURCE3} | tar xvf - -C $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE8} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

rm -f doc/{*,*/*}.sgml

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
%doc CHANGES CREDITS README doc/*.txt
%attr(754,root,root) /etc/rc.d/init.d/console
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/console
%attr(755,root,root) /etc/profile.d/console.*

%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%{_ldatadir}/console*
%{_ldatadir}/keymaps
%{_ldatadir}/unimaps

%{_mandir}/man?/*
%lang(cs) %{_mandir}/cs/man?/*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fi) %{_mandir}/fi/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(hu) %{_mandir}/hu/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(ko) %{_mandir}/ko/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(pt) %{_mandir}/pt/man?/*
%lang(ru) %{_mandir}/ru/man?/*
