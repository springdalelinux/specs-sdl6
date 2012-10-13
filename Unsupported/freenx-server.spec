%bcond_with oldx11

%define _pkglibdir %{_libdir}/nx
%define _pkgdatadir %{_datadir}/nx
%define _pkglibexecdir %{_libexecdir}/nx

Summary: Free Software (GPL) Implementation of the NX Server
Name: freenx-server
Version: 0.7.3
Release: 22%{?dist}
License: GPLv2
Group: Applications/Internet
URL: http://freenx.berlios.de/
Source0: http://download.berlios.de/freenx/%{name}-%{version}.tar.gz
Source1: freenx.logrotate
Patch0: freenx-server-0.7.3-lp-fixes.patch
Patch1: freenx-server-r104-fixes.patch
Patch2: restorecon.patch
Patch3: freenx-server-0.7.3-nxpath-616993.patch
Patch4: freenx-server-0.7.3-nxdialog-627010.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: imake, redhat-release
Requires: nx, %{_pkglibdir}
Requires: openssh-server nc expect which perl
Requires: xorg-x11-server-Xorg xorg-x11-apps
Requires: /usr/lib/cups/backend
%if %{with oldx11}
Requires: fonts-xorg-base
%else
Requires: xorg-x11-fonts-misc
%endif

Obsoletes: freenx < %{version}-%{release}
Provides: freenx = %{version}-%{release}

%description
NX is an exciting new technology for remote display. It provides near
local speed application responsiveness over high latency, low
bandwidth links. The core libraries for NX are provided by NoMachine
under the GPL. FreeNX-server is a GPL implementation of the NX Server.

%prep
%setup -q
%patch0 -p1 -b .lp
%patch1 -p1 -b .fixes
%patch2 -p0 -b .restorecon
%patch3 -p1 -b .nxpath
%patch4 -p1 -b .nxdialog

sed -i -e's,\$NX_DIR/bin,%{_pkglibexecdir},g'\
  -e's,\$NX_DIR/lib,%{_pkglibdir},g'\
  nxloadconfig nxserver
sed -i -e's,^NX_LOGFILE=.*,NX_LOGFILE=/var/log/nx/nxserver.log,' \
  nxloadconfig

%build
CFLAGS="%{optflags}"; export CFLAGS
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} NX_ETC_DIR=/etc/nxserver
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_pkglibexecdir}/nx{setup,keygen} %{buildroot}%{_sbindir}
cp -a %{buildroot}/etc/nxserver/node.conf.sample \
      %{buildroot}/etc/nxserver/node.conf

touch \
 %{buildroot}/etc/nxserver/users.id_dsa \
 %{buildroot}/etc/nxserver/users.id_dsa.pub \
 %{buildroot}/etc/nxserver/client.id_dsa.key \
 %{buildroot}/etc/nxserver/server.id_dsa.pub.key

# Create the nx user home
mkdir -p %{buildroot}/var/lib/nxserver/home/.ssh
ln -s /etc/nxserver/server.id_dsa.pub.key \
  %{buildroot}/var/lib/nxserver/home/.ssh/authorized_keys2
chmod 0700 %{buildroot}/var/lib/nxserver/home{,/.ssh}
touch %{buildroot}/var/lib/nxserver/home/.ssh/known_hosts
mkdir -p %{buildroot}/var/lib/nxserver/db/closed
mkdir -p %{buildroot}/var/lib/nxserver/db/running
mkdir -p %{buildroot}/var/lib/nxserver/db/failed
chmod -R 0700 %{buildroot}/var/lib/nxserver

mkdir -p %{buildroot}/var/log/nx
chmod 0700 %{buildroot}/var/log/nx

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/freenx-server

mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -p init.d/freenx-server %{buildroot}%{_sysconfdir}/init.d/freenx-server

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -r -d /var/lib/nxserver/home -s %{_pkglibexecdir}/nxserver nx 2>/dev/null \
  || %{_sbindir}/usermod -d /var/lib/nxserver/home -s %{_pkglibexecdir}/nxserver nx 2>/dev/null || :

%post
/sbin/chkconfig --add freenx-server
# Not a real service, just to make sure we have /tmp/.X11-unix
/sbin/service freenx-server start > /dev/null 2>&1

%preun
if [ $1 = 0 ]; then
        /sbin/service freenx-server stop > /dev/null 2>&1
        /sbin/chkconfig --del freenx-server
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog CONTRIB
%{_sbindir}/nx*
%{_pkglibexecdir}/*
%{_pkglibdir}/*
/usr/lib/cups/backend/nxsmb
%dir %attr(-,nx,root) /etc/nxserver
/etc/nxserver/node.conf.sample
%config(noreplace) /etc/nxserver/node.conf
%ghost %attr(-,nx,root) /etc/nxserver/users.id_dsa
%ghost %attr(-,nx,root) /etc/nxserver/users.id_dsa.pub
%ghost %attr(-,nx,root) /etc/nxserver/client.id_dsa.key
%ghost %attr(-,nx,root) /etc/nxserver/server.id_dsa.pub.key
%attr(-,nx,root) /var/lib/nxserver
%ghost %attr(-,nx,root) /var/lib/nxserver/home/.ssh/known_hosts
%attr(-,nx,root) /var/log/nx
%config(noreplace) %{_sysconfdir}/logrotate.d/freenx-server
%{_sysconfdir}/init.d/freenx-server

%changelog
* Mon Jun 20 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-22
- Fix nxdialog when /usr/bin/dialog is available but xterm isn't (#627010).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-20
- Fix incorrect service start status when restorecon doesn't exist.

* Wed Jul 21 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-19
- Apply improvements from Fedora bug #616993:
- Install nxkeygen and nxsetup symlinks in /usr/sbin.
- Patch nxkeygen and nxsetup to work when invoked via a symlink.
- Drop nxsetup from docs.

* Mon Nov 23 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-17
- Rebase to launchpad development bzr code.
- Add status to init file.
- Fix persistent session switch.
- Use md5sum (instead of openssl md5) for consistent hashes.

* Sat Jul 25 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-14
- Use some patches from up to svn 613 (dated 2008-09-01).
- Add keymap.patch from Fedora bug #506470.
- Add cups listing patch from Fedora bug #509879.
- Add dependency for misc fonts Fedora bug #467494.
- Fix stale X11 displays from Fedora bug #492402.
- Fix authorized_keys*2* syncing, may fix Fedora bug #503822.
- Move %%post parts to nxserver startup, fixes Fedora bug #474720.
- Copy ssh keys on first start, fixes Fedora bug #235592.
- Add init script with CentOS patches that ensures /tmp/.X11-unix
  always exists, fixes Fedora bug #437655.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-11
- Rebase patch to 0.7.2 to avoid fuzz=0 rejection on recent rpm.
- Update to 0.7.3.
- NX_ETC_DIR needs to be passed on command line (workaround).

* Tue Apr  8 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.2-7
- Rename the logrotate file to match the package name.

* Sat Mar 29 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.2-6
- Update to 0.7.2.
- Upstream project renamed to freenx-server.

* Mon Dec 31 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.1-4
- Apply Jeffrey J. Kosowsky's patches to enable multimedia and
  file/print sharing support (Fedora bug #216802).
- Silence %%post output, when openssh's server has never been started
  before (Fedora bug #235592).
- Add dependency on which (Fedora bug #250343).

* Mon Dec 10 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-3
- Fix syntax error in logrotate file, BZ 418221.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-2
- Added logrotate, BZ 379761.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-1
- Update to 0.7.1, many bugfixes, BZ 364751, 373771.

* Sun Sep 23 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.7.0-2
- Do not try to set up KDE_PRINTRC if ENABLE_KDE_CUPS is not 1, deal better
  with errors when it is (#290351).

* Thu Sep 6 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.0-1
- CM = Christian Mandery mail@chrismandery.de,  BZ 252976
- Version bump to 0.7.0 upstream release (CM)
- Fixed download URL (didn't work, Berlios changed layout). (CM)
- Changed license field from GPL to GPLv2 in RPM. (CM)
- Fixed release.

* Mon Feb 19 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.0-9
- Update to 0.6.0.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.4.

* Sat Jul 30 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.2.

* Sat Jul  9 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.1.

* Tue Mar 22 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.1
- Updated to 0.3.1 release

* Tue Mar 08 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.0
- Updated to 0.3.0 release
- Removed home directory patch as it is now default

* Mon Feb 14 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.8
- Updated to 0.2.8 release
- Fixes some security issues
- Added geom-fix patch for windows client resuming issues

* Thu Dec 02 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.7
- Fixed package removal not removing the var session directories

* Tue Nov 23 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.7
- Updated to 0.2.7 release
- fixes some stability issues with 0.2.6

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.6
- Fixed a problem with key backup upon removal

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.6
- Updated to 0.2.6 release
- Changed setup to have nx user account added as a system account.
- Changed nx home directory to /var/lib/nxserver/nxhome

* Thu Oct 14 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.5
- updated package to 0.2.5 release
- still applying patch for netcat and useradd

* Fri Oct 08 2004 Rick Stout <zipsonic[AT]gmail.com> - 3:0.2.4
- Added nxsetup functionality to the rpm
- patched nxsetup (fnxncuseradd) script for occasional path error.
- Added patch (fnxncuseradd) to resolve newer client connections (netcat -> nc)
- Changed name to be more friendly (lowercase)
- Added known dependencies

* Thu Sep 30 2004 Rick Stout <zipsonic[AT]gmail.com> - 2:0.2.4
- Patch (fnxpermatch) to fix permissions with key generation

* Wed Sep 29 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.4
- Initial Fedora RPM release.
- Updated SuSE package for Fedora
