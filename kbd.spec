Summary:	Linux console utilities
Summary(pl):	Narzêdzia do obs³ugi konsoli
Name:		kbd
Version:	1.05
Release:	1
License:	GPL
Group:		Applications/Console
Group(de):	Applikationen/Konsole
Group(pl):	Aplikacje/Konsola
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/kbd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-install.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gzip
BuildRequires:	gettext-devel
Prereq:		/sbin/chkconfig
Obsoletes:	console-tools
Obsoletes:	console-data
Provides:	console-tools
Provides:	console-data
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains utilities to load console fonts and keyboard
maps. It also includes a number of different fonts and keyboard maps.

%description -l pl
Pakiet zawiera narzêdzia do ³adowania fontów konsolowych oraz map
klawiatury. Dodaktowo do³±czono znaczn± liczbê ró¿nych fontów i map.

%prep
%setup  -q 
%patch0 -p1

%build
./configure \
	--datadir=%{_datadir}/%{name}
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

ln -sf /bin/loadkeys $RPM_BUILD_ROOT%{_bindir}/loadkeys

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/console
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/console

rm -f doc/{*,*/*}.sgml
gzip -9nf CHANGES CREDITS README doc/*.txt

%find_lang %{name}

%post
/sbin/chkconfig --add console
/sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz doc
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/console
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/console

%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/kbd
%{_mandir}/man?/*
