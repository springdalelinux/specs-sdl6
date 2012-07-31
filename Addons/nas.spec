Name:		nas	
Summary:	The Network Audio System (NAS)
Version:	1.9.1
Release:	2%{?dist}
BuildRequires:	bison flex
%if "%{?fedora}" > "4" || "%{?rhel}" > "4"
BuildRequires:	imake libXaw-devel libXpm-devel libXp-devel libXext-devel libXt-devel 
%define libdir_x11 %{_libdir}/X11
%else
BuildRequires: xorg-x11-devel 
# don't rely on (potentially broken) /usr/lib/X11 symlink anyway
%define libdir_x11 %{_prefix}/X11R6/lib/X11
%endif

URL:		http://nas.codebrilliance.com		

License: 	Public Domain
Group: 		Development/Libraries
Source0: 	http://nas.codebrilliance.com/nas/nas-%{version}.src.tar.gz
Source1:	http://apt.kde-redhat.org/apt/kde-redhat/SOURCES/nas/nasd.init
Source2:	http://apt.kde-redhat.org/apt/kde-redhat/SOURCES/nas/nasd.sysconfig

Buildroot: 	%{_tmppath}/NAS-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(preun): chkconfig /sbin/service
Requires(post):  chkconfig

%package devel
Summary:	Development and doc files for the NAS 
Requires:	%{name} = %{version}-%{release}
Group:		Development/Libraries

%description
In a nutshell, NAS is the audio equivalent of an X display  server.
The Network Audio System (NAS) was developed by NCD for playing,
recording, and manipulating audio data over a network.  Like the
X Window System, it uses the client/server model to separate
applications from the specific drivers that control audio input
and output devices.
Key features of the Network Audio System include:
	o  Device-independent audio over the network
	o  Lots of audio file and data formats
	o  Can store sounds in server for rapid replay
	o  Extensive mixing, separating, and manipulation of audio data
	o  Simultaneous use of audio devices by multiple applications
	o  Use by a growing number of ISVs
	o  Small size
	o  Free!  No obnoxious licensing terms

%description devel
Development files and the documentation


%prep
%setup -q -n nas-%{version}
iconv --from-code=ISO_8859-15 --to-code=UTF-8 HISTORY >HISTORY.tmp
mv HISTORY.tmp HISTORY

%build
xmkmf
find . -name Makefile \
| xargs sed -i -e 's/^\(\s*CDEBUGFLAGS\s*=.*\)/\1 $(RPM_OPT_FLAGS)/'
make %{?_smp_mflags} World


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} INCROOT=%{_includedir} \
  LIBDIR=%{libdir_x11}  SHLIBDIR=%{_libdir} USRLIBDIR=%{_libdir} MANPATH=%{_mandir} \
  install install.man

install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/nasd
install -p -m644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nasd

#remove satic lib
rm $RPM_BUILD_ROOT%{_libdir}/*.a
#rename cofigfile
mv $RPM_BUILD_ROOT/etc/nas/nasd.conf.eg $RPM_BUILD_ROOT/etc/nas/nasd.conf

%post
/sbin/ldconfig
/sbin/chkconfig --add nasd

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
  /sbin/chkconfig --del nasd
  /sbin/service nasd stop >/dev/null 2>&1 ||:
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /etc/nas
%config (noreplace) /etc/nas/nasd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/nasd
%{_initrddir}/nasd

%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/libaudio.so.2
%{_libdir}/libaudio.so.2.4
%{libdir_x11}/AuErrorDB
%doc README FAQ HISTORY TODO

%files devel
%defattr(-,root,root)
%{_includedir}/audio/
%{_libdir}/libaudio.so
%{_mandir}/man3/*


%changelog 
*Sun Nov 11 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9.1-2
 - fix spec file
*Sun Nov 11 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9.1-1
 - update to 1.9.1
 - remove unneeded patches

*Fri Nov 02 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-3
 - add better patch for #247468 

*Fri Nov 02 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-2
 - add patch to fix #247468

*Sun Oct 28 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-1
 - update to 1.9a to fix #245712

*Sat Aug 18 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-4
 - fix for bug #245712

* Sat Aug 11  2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-3
 - fix for bug #250453

* Fri May 04 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-2%{?dist}
- rebuild for the new ppc64 arch

* Sun Apr 08 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-1%{?dist}
- update to 1.9
- remove old patch file

* Mon Mar 26 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8b-1%{?dist}
- update to 1.8b

* Thu Mar 22 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8a-2%{?dist}
- use the SVN version of 1.8a

* Wed Mar 21 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8a-1%{?dist}
- fix bug 233353 

* Thu Feb 09 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8-13%{?dist}
- use the corrected patch

* Thu Feb 08 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8-11%{?dist}
- fix bug 227759

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.8-10
- don't rely-on/use potentially broken %%_libdir/X11 symlink (#207180)

* Mon Sep 11 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-9%{?dist}
- second rebuild for FC6

* Mon Jul 24 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-8%{?dist}
- fix ugly output when starting the daemon

* Fri Jul 21 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-7%{?dist}
- disable build for EMT64 on FC4

* Thu Jul 13 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-6%{?dist}
- fix build on EMT64 

* Wed Jul 12 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-5%{?dist}
- fix include dir

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-4%{?dist}
- add Requires(preun): chkconfig /sbin/service
- add Requires(post):  chkconfig
- add remarks for FC4

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-3%{?dist}
- move man3 to devel
- rename nasd.conf.eg to .conf
- add build depend for libXext-devel libXt-devel
- change license to Public Domain
- add path to make intall
- add rc.d/sysconfig  files 

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-2%{?dist}
- move libaudio.so.2 to main package
- switch package name from NAS to nas
- fix depend for devel package
- fix version
- add nas subdir in etc to main package
- set license to Distributable
- add readme file

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-1%{?dist}
- start
