%define zmuid $(id -un)
%define zmgid $(id -gn)
%define zmuid_final apache
%define zmgid_final apache

Name:       zoneminder
Version:    1.25.0
Release:    6%{?dist}
Summary:    A camera monitoring and analysis tool
Group:      System Environment/Daemons
# jscalendar is LGPL (any version):  http://www.dynarch.com/projects/calendar/
# Mootools is inder the MIT license: http://mootools.net/
License:    GPLv2+ and LGPLv2+ and MIT 
URL:        http://www.zoneminder.com/

Source:     http://www2.zoneminder.com/downloads/ZoneMinder-%{version}.tar.gz
Source2:    zoneminder.conf
Source3:    redalert.wav
Source4:    README.Fedora
Source5:    http://downloads.sourceforge.net/jscalendar/jscalendar-1.0.zip
Source6:    zoneminder.service
Source7:    zoneminder.logrotate
# Need to unravel the proper mootools files to grab from upstream, since the
# number of them keeps multiplying.  In the meantime, rely on the ones bundled
# with zoneminder.  As these are javascript, there is no guideline violation
# here.
#Source8:    http://mootools.net/download/get/mootools-1.2.3-core-yc.js
Patch1:     zoneminder-1.25.0-dbinstall.patch
Patch2:     zoneminder-1.24.3-runlevel.patch
Patch3:     zoneminder-1.25.0-noffmpeg.patch
Patch10:    zoneminder-1.24.4-installfix.patch
Patch11:    zoneminder-1.25.0-gcc47.patch
Patch12:    zoneminder-1.25.0-gcrypt.patch

BuildRequires:  automake gnutls-devel
BuildRequires:  mysql-devel pcre-devel libjpeg-devel
BuildRequires:  perl(Archive::Tar) perl(Archive::Zip)
BuildRequires:  perl(Date::Manip) perl(DBD::mysql)
BuildRequires:  perl(ExtUtils::MakeMaker) perl(LWP::UserAgent)
BuildRequires:  perl(MIME::Entity) perl(MIME::Lite)
BuildRequires:  perl(PHP::Serialization) perl(Sys::Mmap)
BuildRequires:  perl(Time::HiRes)

Requires:   httpd php php-mysql cambozola
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:   perl(DBD::mysql) perl(Archive::Tar) perl(Archive::Zip)
Requires:   perl(MIME::Entity) perl(MIME::Lite) perl(Net::SMTP) perl(Net::FTP)

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service


%description
ZoneMinder is a set of applications which is intended to provide a complete
solution allowing you to capture, analyse, record and monitor any cameras you
have attached to a Linux based machine. It is designed to run on kernels which
support the Video For Linux (V4L) interface and has been tested with cameras
attached to BTTV cards, various USB cameras and IP network cameras. It is
designed to support as many cameras as you can attach to your computer without
too much degradation of performance.


%prep
%setup -q -n ZoneMinder-%{version}

# Unpack jscalendar and move some files around
%setup -q -D -T -a 5 -n ZoneMinder-%{version}
mkdir jscalendar-doc
pushd jscalendar-1.0
mv *html *php doc/* README ../jscalendar-doc
rmdir doc
popd

%patch1 -p0 -b .dbinstall
%patch2 -p0 -b .runlevel
%patch3 -p0 -b .noffmpeg
%patch10 -p0 -b .installfix
%patch11 -p0 -b .gcc47
%patch12 -p0 -b .gcrypt
cp %{SOURCE4} README.Fedora
chmod -x src/zm_event.cpp src/zm_user.h


%build
autoreconf

OPTS=""
%ifnarch %{ix86} x86_64
    OPTS="$OPTS --disable-crashtrace"
%endif

export ZM_RUNDIR=/var/run/zoneminder
export ZM_TMPDIR=/var/lib/zoneminder/temp
%configure \
    --with-libarch=%{_lib} \
    --with-mysql=%{_prefix} \
    --with-webdir=%{_datadir}/%{name}/www \
    --with-cgidir=%{_libexecdir}/%{name}/cgi-bin \
    --with-webuser=%{zmuid} \
    --with-webgroup=%{zmgid} \
    --enable-mmap=yes \
    --disable-debug \
    $OPTS

# Have to do this now because the configure script wipes out modifications made to this file
cat <<EOF >> db/zm_create.sql
# Fedora change:
# Alter some default paths to match the default URL and selinux expectations
update Config set Value = '/cgi-bin/zm/nph-zms' where Name = 'ZM_PATH_ZMS';
update Config set Value = '/var/log/zoneminder' where Name = 'ZM_PATH_LOGS';
update Config set Value = '/var/log/zoneminder/zm_debug_log+' where Name = 'ZM_EXTRA_DEBUG_LOG';
update Config set Value = '/var/log/zoneminder/zm_xml.log' where Name = 'ZM_EYEZM_LOG_FILE';
update Config set Value = '/var/lib/zoneminder/sock' where Name = 'ZM_PATH_SOCKS';
update Config set Value = '/var/lib/zoneminder/swap' where Name = 'ZM_PATH_SWAP';
update Config set Value = '/var/spool/zoneminder-upload' where Name = 'ZM_UPLOAD_FTP_LOC_DIR';
EOF

make %{?_smp_mflags}
%{__perl} -pi -e 's/(ZM_WEB_USER=).*$/${1}%{zmuid_final}/;' \
          -e 's/(ZM_WEB_GROUP=).*$/${1}%{zmgid_final}/;' zm.conf


%install
install -d %{buildroot}/%{_localstatedir}/run
make install DESTDIR=%{buildroot} \
    INSTALLDIRS=vendor
rm -rf %{buildroot}/%{perl_vendorarch} %{buildroot}/%{perl_archlib}
rm -f %{buildroot}/%{_bindir}/zmx10.pl

install -m 755 -d %{buildroot}/var/log/zoneminder
for dir in events images temp
do
    install -m 755 -d %{buildroot}/var/lib/zoneminder/$dir
    rmdir %{buildroot}/%{_datadir}/zoneminder/www/$dir
    ln -sf ../../../../var/lib/zoneminder/$dir %{buildroot}/%{_datadir}/zoneminder/www/$dir
done
install -m 755 -d %{buildroot}/var/lib/zoneminder/sock
install -m 755 -d %{buildroot}/var/lib/zoneminder/swap
install -m 755 -d %{buildroot}/var/spool/zoneminder-upload

install -D -m 755 scripts/zm %{buildroot}/%{_initrddir}/zoneminder
install -D -m 644 %{SOURCE2} %{buildroot}/etc/httpd/conf.d/zoneminder.conf
install -D -m 755 %{SOURCE3} %{buildroot}/%{_datadir}/zoneminder/www/sounds/redalert.wav
install -D -m 644 %{SOURCE7} %{buildroot}/etc/logrotate.d/zoneminder

# Install jscalendar - this really should be in its own package
install -d -m 755 %{buildroot}/%{_datadir}/%{name}/www/jscalendar
cp -rp jscalendar-1.0/* %{buildroot}/%{_datadir}/zoneminder/www/jscalendar

# Set up cambozola
pushd %{buildroot}/%{_datadir}/zoneminder/www
ln -s ../../java/cambozola.jar
popd

install -d -m 755 %{buildroot}/etc/tmpfiles.d
cat > %{buildroot}/etc/tmpfiles.d/zoneminder.conf <<EOF
d   /run/zoneminder     0755    %{zmuid_final}  %{zmgid_final}
EOF
install -m 755 -d %{buildroot}/run/zoneminder


%post
/sbin/chkconfig --add zoneminder


%preun
if [ $1 -eq 0 ]; then
    /sbin/service zoneminder stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del zoneminder
fi


%postun
if [ $1 -ge 1 ]; then
    /sbin/service zoneminder condrestart > /dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README README.Fedora jscalendar-doc
%config(noreplace) %attr(640,root,%{zmgid_final}) /etc/zm.conf
%config(noreplace) %attr(644,root,root) /etc/httpd/conf.d/zoneminder.conf
%config(noreplace) /etc/tmpfiles.d/zoneminder.conf
%config(noreplace) /etc/logrotate.d/zoneminder

%attr(755,root,root) %{_initrddir}/zoneminder

%{_bindir}/zma
%{_bindir}/zmaudit.pl
%{_bindir}/zmc
%{_bindir}/zmcontrol.pl
%{_bindir}/zmdc.pl
%{_bindir}/zmf
%{_bindir}/zmfilter.pl
%attr(4755,root,root) %{_bindir}/zmfix
%{_bindir}/zmpkg.pl
%{_bindir}/zmstreamer
%{_bindir}/zmtrack.pl
%{_bindir}/zmtrigger.pl
%{_bindir}/zmu
%{_bindir}/zmupdate.pl
%{_bindir}/zmvideo.pl
%{_bindir}/zmwatch.pl

%{perl_vendorlib}/ZoneMinder*
%{_mandir}/man*/*
%dir %{_libexecdir}/zoneminder
%{_libexecdir}/zoneminder/cgi-bin
%dir %{_datadir}/zoneminder
%{_datadir}/zoneminder/db
%{_datadir}/zoneminder/www

%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder/events
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder/images
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder/sock
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder/swap
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/lib/zoneminder/temp
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/log/zoneminder
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /var/spool/zoneminder-upload
%dir %attr(755,%{zmuid_final},%{zmgid_final}) /run/zoneminder


%changelog
* Wed Mar 21 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-6
- Fix stupid thinko in sql modifications.

* Sat Feb 25 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-5
- Clean up macro usage.

* Sat Feb 25 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-4
- Convert to systemd.
- Add tmpfiles.d configuration since the initscript isn't around to create
  /run/zoneminder.
- Remove some pointless executable permissions.
- Add logrotate file.

* Wed Feb 22 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-3
- Update README.Fedora to reference systemctl and mention timezone info in
  php.ini.
- Add proper default for EYEZM_LOG_TO_FILE.


* Thu Feb 09 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-2
- Rebuild for new pcre.

* Thu Jan 19 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.25.0-1
- Update to 1.25.0
- Fix gcc4.7 build problems.
- Drop gcc4.4 build fixes; for whatever reason they now break the build.
- Clean up old patches.
- Force setting of ZM_TMPDIR and ZM_RUNDIR.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.4-3
- Re-add the dist-tag that somehow got lost.

* Thu Sep 15 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.4-2
- Add patch for bug 711780 - fix syntax issue in Mapped.pm.
- Undo that patch, and undo another which was the cause of the whole mess.
- Fix up other patches so ZM_PATH_BUILD is both defined and useful.
- Make sure database creation mods actually take.
- Update Fedora-specific docs with some additional info.
- Use bundled mootools (javascript, so no guideline violation).
- Update download location.
- Update the gcrypt patch to actually work.
- Upstream changed the tarball without changing the version to patch a
  vulnerability, so redownload.

* Sun Aug 14 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.4-1
- Initial attempt to upgrade to 1.24.4.
- Add patch from BZ 460310 to build against libgcrypt instead of requiring the
  gnutls openssl libs.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.24.3-7.20110324svn3310
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.24.3-6.20110324svn3310
- Perl mass rebuild

* Mon May 09 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.3-5.20110324svn3310
- Bump for gnutls update.

* Thu Mar 24 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.3-4.20110324svn3310
- Update to latest 1.24.3 subversion.  Turns out that what upstream was calling
  1.24.3 is really just an occasionally updated devel snapshot.
- Rebase various patches.

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.24.3-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.3-1
- Update to latest upstream version.
- Rebase patches.
- Initial incomplete attempt to disable v4l1 support.

* Fri Jan 21 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.2-6
- Unbundle cambozola; instead link to the separately pacakged copy.
- Remove BuildRoot:, %%clean and buildroot cleaning in %%install.
- Git rid of mixed space/tab usage by removing all tabs.
- Remove unnecessary Conflicts: line.
- Attempt to force short_open_tag on for the code directories.
- Move default location of sockets, swaps, logfiles and some temporary files to
  make more sense and allow things to work better with a future selinux policy.
- Fix errors in README.Fedora.

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24.2-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.24.2-4
- rebuild against perl 5.10.1
- use Perl vendorarch and archlib variables correctly

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.2-2
- Bump release since 1.24.2-1 was mistakenly tagged a few months ago.

* Wed Jul 22 2009 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.24.2-1
- Initial update to 1.24.2.
- Rebase patches.
- Update mootools download location.
- Update to mootools 1.2.3.
- Add additional dependencies for some optional features.

* Sat Apr 11 2009 Martin Ebourne <martin@zepler.org> - 1.24.1-3
- Remove unused Sys::Mmap perl dependency RPM is finding

* Sat Apr 11 2009 Martin Ebourne <martin@zepler.org> - 1.24.1-2
- Update gcc44 patch to disable -frepo, seems to be broken with gcc44
- Added noffmpeg patch to make building outside mock easier

* Sat Mar 21 2009 Martin Ebourne <martin@zepler.org> - 1.24.1-1
- Patch for gcc 4.4 compilation errors
- Upgrade to 1.24.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 1.23.3-3
- rebuild for dependencies

* Mon Dec 15 2008 Martin Ebourne <martin@zepler.org> - 1.23.3-2
- Fix permissions on zm.conf

* Fri Jul 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.23.3-1
- Initial attempt at packaging 1.23.

* Tue Jul  1 2008 Martin Ebourne <martin@zepler.org> - 1.22.3-15
- Add perl module compat dependency, bz #453590

* Tue May  6 2008 Martin Ebourne <martin@zepler.org> - 1.22.3-14
- Remove default runlevel, bz #441315

* Mon Apr 28 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.22.3-13
- Backport patch for CVE-2008-1381 from 1.23.3 to 1.22.3.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.22.3-12
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Martin Ebourne <martin@zepler.org> - 1.22.3-11
- Fix compilation on gcc 4.3

* Thu Dec  6 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-10
- Rebuild for new openssl

* Thu Aug  2 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-8
- Fix licence tag

* Thu Jul 12 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-7
- Fixes from testing by Jitz including missing dependencies and database creation

* Sat Jun 30 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-6
- Disable crashtrace on ppc

* Sat Jun 30 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-5
- Fix uid for directories in /var/lib/zoneminder

* Tue Jun 26 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-4
- Added perl Archive::Tar dependency
- Disabled web interface due to lack of access control on the event images

* Sun Jun 10 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-3
- Changes recommended in review by Jason Tibbitts

* Mon Apr  2 2007 Martin Ebourne <martin@zepler.org> - 1.22.3-2
- Standardised on package name of zoneminder

* Thu Dec 28 2006 Martin Ebourne <martin@zepler.org> - 1.22.3-1
- First version. Uses some parts from zm-1.20.1 by Corey DeLasaux and Serg Oskin
