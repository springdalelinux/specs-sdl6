Summary:	An RTMP server implemented in C++
Name: 		crtmpserver
Version:	775
Release:	1.1%{?dist}
License:	GPLv3+
Vendor:		rtmpd.com
Group:		System Environment/Daemons
URL:		http://www.rtmpd.com

# Sources
Source:		%{name}-%{version}.tar.gz
Source1:	crtmpserver.init

# Patches
Patch0:		crtmpserver.lua.patch

# Dependencies
BuildRequires:	perl cmake make gcc gcc-c++ openssl-devel zlib-devel lua-devel tinyxml-devel
Requires:	coreutils lua

%Description
crtmpserver it is a high performance streaming server able to stream (live or recorded) in the following technologies:

- To and from Flash (RTMP,RTMPE, RTMPS, RTMPT, RTMPTE)
- To and from embedded devices: iPhone, Android
- From surveillance cameras
- IP-TV using MPEG-TS and RTSP/RTCP/RTP protocols

Also, crtmpserver can be used as a high performance rendes-vous server. For example, it enables you to do:

- Audio/Video conferencing
- Online gaming
- Online collaboration
- Simple/complex chat applications

%prep
%setup
#echo name=%{name}, version=%{version}, _tmppath=%{_tmppath}, pfx=%{pfx}, RPM_BUILD_ROOT=$RPM_BUILD_ROOT
%patch0 -p1

cd builders/cmake
%if "lib" != "%{_lib}"
perl -pi -e 's|lib/crtmpserver|%{_lib}/%{name}|' CMakeLists.txt crtmpserver/crtmpserver.lua
%endif

%build
cd builders/cmake
cmake -DCRTMPSERVER_INSTALL_PREFIX=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
cd builders/cmake
make install DESTDIR=$RPM_BUILD_ROOT
# move other things into place
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv $RPM_BUILD_ROOT/usr/man/man1 $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/etc/crtmpserver
mv $RPM_BUILD_ROOT/usr/etc/crtmpserver.lua.sample $RPM_BUILD_ROOT/etc/crtmpserver/crtmpserver.lua
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/%{name}
mkdir -p $RPM_BUILD_ROOT/srv/media

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/id crtmpserver >/dev/null 2>&1 || \
        /usr/sbin/useradd -r -c 'crtmpserver' -s /sbin/nologin -d / crtmpserver

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root)
%{_sbindir}/crtmpserver
%{_libdir}/%{name}
%{_mandir}/man1/*
%dir /etc/crtmpserver
%config(noreplace) /etc/crtmpserver/*
%{_initddir}/%{name}
%attr(755, crtmpserver, crtmpserver) %dir /srv/media

%changelog
* Sun Jun  3 2012 Peter Ajamian <peter@pajamian.dhs.org> - 775-1.1
- Bump to latest SVN
- Build from trunk instead of 1.0 branch
- Set default media directory to /srv/media

* Wed May 30 2012 Peter Ajamian <peter@pajamian.dhs.org> - 768-1.0
- Bump to latest SVN
- Start daemon with the correct gid

* Sun May 27 2012 Peter Ajamian <peter@pajamian.dhs.org> - 717-1.3
- Fix license to GPLv3+
- Fix missing group error in %pre
- Fix init.d script error caused by missing ";;" in case blocks
- Added perl, make, gcc and gcc-c++ to BuildRequires
- Use the id command to get the crtmpserver uid in init.d script
- Added coreutils to Requires
- Removed unneeded whitespace from DAEMON_ARGS and DEMON_UID_ARG in init.d script
- Changed init.d script hashbang to bin/bash to make sure that we invoke it in bash
- Fix daemon line in init.d script to use the --pid switch instead of --pidfile
- Other minor cosmetic fixes to the init.d script
- Patch config file for a reasonable working default install and install as the real
  config file and not a sample, also install as noreplace

* Tue May 22 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build based on a few different things
