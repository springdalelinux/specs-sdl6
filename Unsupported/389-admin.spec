%global pkgname   dirsrv
# for a pre-release, define the prerel field - comment out for official release
# % global prerel .a1
# also need the relprefix 0. field for a pre-release - also comment out for official release
# % global relprefix 0.

Summary:          389 Administration Server (admin)
Name:             389-admin
Version:          1.1.23
Release:          %{?relprefix}1%{?prerel}%{?dist}
License:          GPLv2 and ASL 2.0
URL:              http://port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    openldap-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    httpd-devel
BuildRequires:    apr-devel
BuildRequires:    mod_nss
BuildRequires:    389-adminutil-devel

Requires:         389-ds-base
Requires:         mod_nss

# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python

# this is needed to load and unload the policy module
Requires(post):         policycoreutils
Requires(preun):        policycoreutils
Requires(postun):       policycoreutils

# the following are needed for some of our scripts
Requires:         perl-Mozilla-LDAP
Requires:         nss-tools

# for the init script
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

Source0:          http://port389.org/sources/%{name}-%{version}%{?prerel}.tar.bz2
# 389-admin-git.sh should be used to generate the source tarball from git
Source1:          %{name}-git.sh

%description
389 Administration Server is an HTTP agent that provides management features
for 389 Directory Server.  It provides some management web apps that can
be used through a web browser.  It provides the authentication, access control,
and CGI utilities used by the console.

%prep
%setup -q -n %{name}-%{version}%{?prerel}

%build
%configure --disable-rpath --with-selinux --with-openldap --enable-service

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 

make DESTDIR="$RPM_BUILD_ROOT" install

# make console jars directory
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java

#remove libtool and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/modules/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%pre -p <lua>
-- save ownership/permissions on the dirs/files that rpm changes
-- if these don't exist, the vars will be nil
%{pkgname}admin_adminserv = posix.stat('%{_sysconfdir}/%{pkgname}/admin-serv')
%{pkgname}admin_consoleconf = posix.stat('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf')

%post -p <lua>
-- do the usual daemon post setup stuff
os.execute('/sbin/chkconfig --add %{pkgname}-admin')
os.execute('/sbin/ldconfig')
-- restore permissions if upgrading
if %{pkgname}admin_adminserv then
    posix.chmod('%{_sysconfdir}/%{pkgname}/admin-serv', %{pkgname}admin_adminserv.mode)
    posix.chown('%{_sysconfdir}/%{pkgname}/admin-serv', %{pkgname}admin_adminserv.uid, %{pkgname}admin_adminserv.gid)
end
if %{pkgname}admin_consoleconf then
    posix.chmod('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf', %{pkgname}admin_consoleconf.mode)
    posix.chown('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf', %{pkgname}admin_consoleconf.uid, %{pkgname}admin_consoleconf.gid)
end

%preun
if [ $1 = 0 ]; then
        /sbin/service %{pkgname}-admin stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{pkgname}-admin
fi

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_sysconfdir}/%{pkgname}/admin-serv
%config(noreplace)%{_sysconfdir}/%{pkgname}/admin-serv/*.conf
%{_datadir}/%{pkgname}
%{_sysconfdir}/rc.d/init.d/%{pkgname}-admin
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}-admin
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{pkgname}
%{_mandir}/man8/*

%changelog
* Thu Aug 11 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.23-1
- Bug 730079 - Update SELinux policy during upgrades

* Thu Aug 11 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.22-1
- Bug 724808 - startup CGIs write temp file to /
- add man pages for ds_removal and ds_unregister
- fixes for the makeUpgradeTar.sh script

* Tue Aug  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.21-1
- Bug 476925 - Admin Server: Do not allow 8-bit passwords for the admin user

* Tue Jul  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.20-3
- bump rel to rebuild with 389-adminutil-1.1.14

* Tue Jul  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.20-2
- bump rel to rebuild with 389-adminutil-1.1.14

* Tue Jul  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.20-1
- Bug 719056 - migrate-ds-admin.pl needs to update SELinux policy
- Bug 718285 - AdminServer should use "service" command instead of start/stop/restart scripts
- Bug 718079 - Perl errors when running migrate-ds-admin.pl
- Bug 713000 - Migration stops if old admin server cannot be stopped
- added tests for the security cgi
- fix typo in NSS_Shutdown warning message
- better NSS error handling - reduce memory leaks
- Bug 710372 - Not able to open the Manage Certificate from DS-console

* Thu Jun 30 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.19-2
- bump rev to rebuild with 389-adminutil-1.1.14

* Tue Jun 28 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.19-1
- look for separate openldap ldif library

* Tue Jun 21 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.18-1
- skip rebranding current brand
- support for skins

* Fri May 13 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.17-1
- 1.1.17
- support "in-place" upgrade and rebranding from Red Hat to 389
- many fixes for coverity issues

* Tue Mar 29 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.16-1
- 389-admin-1.1.16
- Bug 476925 - Admin Server: Do not allow 8-bit passwords for the admin user
- Bug 614690 - Don't use exec to call genrb
- Bug 158926 - Unable to install CA certificate when using
-     hardware token ( LunaSA )
- Bug 211296 - Clean up all HTML pages (Admin Express, Repl Monitor, etc)

* Wed Feb 23 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.15-1
- 1.1.15 release - git tag 389-admin-1.1.15
- Bug 493424 - remove unneeded modules for admin server apache config
- Bug 618897 - Wrong permissions when creating instance from Console
- Bug 672468 - Don't use empty path elements in LD_LIBRARY_PATH
- Bug 245278 - Changing to a password with a single quote does not work
- Bug 604881 - admin server log files have incorrect permissions/ownerships
- Bug 387981 - plain files can be chosen on the Restore Directory dialog
- Bug 668950 - Add posix group support to Console
- Bug 618858 - move start-ds-admin env file into main admin server config path
- Bug 616260 - libds-admin-serv linking fails due to unresolved link-time depe
ndencies
- start-ds-admin.in -- replaced "return 1" with "exit 1"
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- Bug 470576 - Migration could do addition checks before commiting actions

* Wed Jan  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.14-1
- 1.1.14 release
- Bug 664671 - Admin server segfault when full SSL access (http+ldap+console) 
required
- Bug 638511 - dirsrv-admin crashes at startup with SELinux enabled

* Mon Nov 29 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.13-2
- fix Conflicts for selinux policy

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.13-1
- This is the final 1.1.13 release
- git tag 389-admin-1.1.13
- Bug 656441 - Missing library path entry causes LD_PRELOAD error
- setup-ds-admin.pl -u exits with ServerAdminID and as_uid related error

* Thu Nov 18 2010 Nathan Kinder <nkinder@redhat.com> - 1.1.12-2
- This is the final 1.1.12 release
- git tag 389-admin-1.1.12
- Corrected conflict version for selinux-policy

* Fri Nov 12 2010 Nathan Kinder <nkinder@redhat.com> - 1.1.1.12-1
- This is the final 1.1.12 release
- git tag 389-admin-1.1.12

* Fri Nov 12 2010 Nathan Kinder <nkinder@redhat.com> - 1.1.1.12-1
- Bug 648949 - Merge dirsrv and dirsrv-admin policy modules into base policy

* Tue Oct 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.12-0.2.a2
- fix mozldap build breakage

* Tue Sep 28 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.12-0.1.a1
- This is the 1.1.12 alpha 1 release - with openldap support

* Thu Aug 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.11-1
- This is the final 1.1.11 release

* Wed Aug  4 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.11-0.7.rc2
- 1.1.11.rc2 release
- git tag 389-admin-1.1.11.rc2
- Bug 594745 - Get rid of dirsrv_lib_t label

* Wed Jun  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.11-0.6.rc1
- 1.1.11.rc1 release

* Wed May 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.11-0.5.a4
- 1.1.11.a4 release

* Tue Apr  7 2010 Nathan Kinder <nkinder@redhat.com> - 1.1.11-0.4.a3
- 1.1.11.a3 release
- Bug 570912 - dirsrv-admin SELinux module fails to install
- Change parsing of start-slapd for instance name
- Bug 574233 - Updated requirements for selinux policy
- Moved selinux subpackage into base package

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.1.11.a2-0.3
- rebuild for icu 4.4

* Fri Feb 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.11.a2-0.2
- the 1.1.11.a2 release
- Bug 460162 - FedoraDS "with-FHS" installs init.d StartupScript in wrong location
- Bug 460209 - Correct configure help message
- Bug 560827 - Admin Server: DistinguishName validation fails
- Make check for threaded httpd work with Apache 2.0

* Thu Jan 21 2010 Nathan Kinder <nkinder@redhat.com> - 1.1.11.a1-0.1
- the 1.1.11.a1 release
- added SELinux subpackage

* Wed Jan 20 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.10-1
- the 1.1.10 release
- allow server to run unconfined if not built with selinux support

* Thu Jan 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.10.a3-0.3
- the 1.1.10.a3 release
- make sure we can find ICU genrb on all platforms

* Fri Dec 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.10.a2-0.2
- the 1.1.10.a2 release
- fix problem with genrb path on F-12 and later

* Thu Oct  8 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.10.a1-1
- the 1.1.10.a1 release

* Mon Sep 14 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.9-1
- the 1.1.9 release

* Tue Aug 25 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-6
- rewrite perm/owner preservation code to use lua

* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-5
- final rebuild for 1.1.8 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-3
- bump rev for final rebuild

* Tue Jul 21 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-2
- change adminutil to 389-adminutil

* Thu Jun 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-1
- bump version to 1.1.8
- change license to GPLv2 + ASL 2.0
- changed files that were incorrectly licensed as GPLv2+ to plain GPLv2

* Wed May 13 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.7-5
- rename to 389

* Thu Apr  9 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.7-4
- Resolves: bug 493424
- Description: dirsrv-admin initscript looks for nonexistent library
- Added patch to remove those modules from the httpd.conf

* Wed Apr  8 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.7-3
- Resolves: bug 494980
- Description: setup-ds-admin.pl -u and silent setup complain about ServerIpAddress
- CVS tag FedoraDirSrvAdmin_1_1_7_RC3 FedoraDirSrvAdmin_1_1_7_RC3_20090408

* Fri Apr  3 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.7-2
- Resolves: bug 493989
- Description: Admin Server: valgrind invalid read in security.c when installing CRL

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.7-1
- this is the 1.1.7 release
- added man pages for setup, migration, remove commands
- better error handling for command line utilities
- fixed remove from console
- added remove-ds-admin.pl
- added pre and post sections in order to preserve the permissions and ownerships
- CVS tag FedoraDirSrvAdmin_1_1_7_RC1 FedoraDirSrvAdmin_1_1_7_RC1_20090331

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.6-2
- patch for bug 451702 not required anymore - in upstream now

* Wed Jul  2 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.6-1
- add patch for bug 451702
- The 1.1.6 release

* Fri Jun  6 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.5-1
- Resolves: Bug 448366
- genrb no longer supports -p option

* Tue Apr 15 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.4-1
- Resolves: Bug 437301
- Directory Server: shell command injection in CGI replication monitor
- Fix: rewrite the perl script to ignore all input parameters - replmon.conf
- file will have to be hard coded to be in the admin-serv directory
- Resolves: Bug 437320
- Directory Server: unrestricted access to CGI scripts
- Fix: remove script alias for /bin/admin/admin/bin/

* Wed Jan  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- Fix issues associated with Fedora pkg review bug 249548

* Tue Dec 11 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- this is the final GA candidate

* Tue Nov  6 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.16
- fix several beta blocker issues

* Mon Oct 15 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.15
- fix bogus dist macro
- change mozldap6 to mozldap

* Thu Oct 11 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.14
- make admin server work with SELinux enabled
- fix wording errors in setup

* Mon Oct  8 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.13
- added /etc/sysconfig/dirsrv-admin the file that allows you to set
- the environment used to start up the admin server (e.g. keytab, ulimit, etc.)
- the initscript and admin start script use this file now
- This version also has a fix to print the correct error message if the admin
- server cannot be contacted during setup or migration.

* Thu Sep 27 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.12
- fix a couple of migration issues, including the rpath $libdir problem
- allow ds_remove from console to remove instances

* Wed Sep 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.11
- one line fix to fix of 295001 - console.conf clobbered

* Tue Sep 18 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.10
- fixed migration issue bugzilla 295001 - console.conf clobbered

* Fri Sep 14 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.9
- fix several more migration problems

* Fri Sep 14 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.8
- fix migration - servers are started as they are migrated now

* Tue Aug 21 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.7
- Fix the with-fhs-opt configure flag

* Fri Aug 17 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.6
- remove curses
- make mod_admserv link against sasl
- add the usual .m4 files to mod_admserv instead of having all of
- the component logic in configure.in

* Thu Aug 16 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.5
- incorporate Noriko's migration fix

* Wed Aug 15 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.4
- address several migration issues

* Mon Aug 13 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.3
- there is no devel package, so remove unused .so files

* Mon Aug 13 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.2
- forgot to tag the modules

* Fri Aug 10 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.1
- get rid of cvsdate
- use pkgname of dirsrv for filesystem path naming
- get rid of devel package
- simplify files section

* Fri Aug 10 2007 Noriko Hosoi <nhosoi@redhat.com> - 1.1.0-0.3.20070810
- updated to latest sources
- upgraded the mozldap6 version to 6.0.4

* Wed Aug  8 2007 Noriko Hosoi <nhosoi@redhat.com> - 1.1.0-0.2.20070808
- updated to latest sources -- bug fixes in the setup scripts

* Mon Aug  6 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070806
- updated to latest sources

* Thu Aug  2 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.4.20070802
- There are no files in bindir anymore

* Thu Aug  2 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.3.20070802
- forgot to prepend build root to java dir creation

* Thu Aug  2 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.2.20070802
- forgot to add mod_admserv and mod_restartd to source

* Thu Aug  2 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070802
- updated to latest sources - fix build breakage
- add console jars dir under html

* Mon Jul 23 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070725
- Initial version based on fedora-ds-base.spec
