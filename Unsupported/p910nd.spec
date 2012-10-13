Summary: Tiny non-spooling printer daemon.
Name: p910nd
Version: 0.93
Release: 1%{?dist}
URL: http://p910nd.sourceforge.net
Vendor: Etherboot project
License: GPL
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: p910nd
BuildRoot: /tmp/%{name}-%{version}
Group: Networking


%description
Tiny non-spooling printer daemon for Linux hosts.
Accepts data over a TCP network connection from
a spooling host. Useful on diskless X terminals
with local printer.

%pre

%prep
rm -rf $RPM_BUILD_ROOT
%setup -n %{name}-%{version}

%build
make ROOT="$RPM_BUILD_ROOT"

%install

mkdir -p $RPM_BUILD_ROOT%{_initddir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/p910nd/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8

install %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/p910nd
install p910nd $RPM_BUILD_ROOT%{_sbindir}
install banner.pl client.pl $RPM_BUILD_ROOT%{_libdir}/p910nd/
install p910nd.8 $RPM_BUILD_ROOT%{_mandir}/man8

%post
/sbin/chkconfig --add p910nd || :

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del p910nd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_initddir}/p910nd
%{_sbindir}/p910nd
%{_libdir}/p910nd
%{_mandir}/man8/p910nd.8*

%changelog
* Mon Jun 14 2010 Josko Plazonic <plazonic@math.princeton.edu>
- version 0.93

* Thu Aug 12 2004 Ken Yap <ken_yap@users.sourceforge.net>
- Version 0.7
- Implemented bidirectional streams (-b option) and improved syslog handling
* Fri Aug 01 2003 Ken Yap <ken_yap@users.sourceforge.net>
- Version 0.6
- Arne Bernin fixed some cast warnings, corrected the version number
and added a -v option to print the version.
* Wed Sep 25 2002 Ken Yap <ken_yap@users.sourceforge.net>
- Version 0.5
- Can compile with libwrap now by defining USE_LIBWRAP and -lwrap
* Thu Apr 12 2001 Ken Yap <ken_yap@users.sourceforge.net>
- Version 0.4
- Added -f flag to specify device other than /dev/lpN
* Fri Nov 19 1999 Ken Yap <ken.yap@acm.org>
- Version 0.3
* Tue Apr 6 1999 Petr Kri¹tof <Petr@Kristof.CZ>
- Initial release
