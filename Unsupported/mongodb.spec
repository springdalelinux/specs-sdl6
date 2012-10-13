# Make sure initddir is defined on el5 and possibly other distros
%{!?_initddir: %define _initddir %{_initrddir}}

%global         daemon mongod

Name:           mongodb
Version:        2.0.3
Release:        8%{?dist}
Summary:        High-performance, schema-free document-oriented database
Group:          Applications/Databases
License:        AGPLv3 and zlib and ASL 2.0
# util/md5 is under the zlib license
# manpages and bson are under ASL 2.0
# everything else is AGPLv3
URL:            http://www.mongodb.org

Source0:        http://fastdl.mongodb.org/src/%{name}-src-r%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}.logrotate
Source3:        %{name}.conf
Source4:        %{daemon}.sysconf
Source5:        %{name}-tmpfile
Source6:        %{daemon}.service
Patch1:         mongodb-no-term.patch
Patch2:         mongodb-fix-fork.patch
# https://github.com/mongodb/mongo/pull/161
Patch3:         mongodb-fix-pcre.patch
# https://github.com/mongodb/mongo/pull/160
Patch4:         mongodb-src-r2.0.2-js.patch
# https://jira.mongodb.org/browse/SERVER-4591
Patch5:         mongodb-fix-oldpython.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  scons
BuildRequires:  boost-devel
BuildRequires:  pcre-devel
BuildRequires:  js-devel
BuildRequires:  readline-devel
BuildRequires:  libpcap-devel
BuildRequires:  snappy-devel

%if 0%{?fedora} >= 15
Requires(post): systemd-units
Requires(preun): systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig
%endif

Requires(pre):  shadow-utils

%if 0%{?fedora} >= 15
Requires(postun): systemd-units
%else
Requires(postun): initscripts
%endif

Requires:       lib%{name} = %{version}-%{release}

# Mongodb must run on a little-endian CPU (see bug #630898)
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x

%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. MongoDB is written in C++ and offers the following
features:
    * Collection oriented storage: easy storage of object/JSON-style data
    * Dynamic queries
    * Full index support, including on inner objects and embedded arrays
    * Query profiling
    * Replication and fail-over support
    * Efficient storage of binary data including large objects (e.g. photos
    and videos)
    * Auto-sharding for cloud-level scalability (currently in early alpha)
    * Commercial Support Available

A key goal of MongoDB is to bridge the gap between key/value stores (which are
fast and highly scalable) and traditional RDBMS systems (which are deep in
functionality).

%package -n lib%{name}
Summary:        MongoDB shared libraries
Group:          Development/Libraries

%description -n lib%{name}
This package provides the shared library for the MongoDB client.

%package devel
Summary:        MongoDB header files
Group:          Development/Libraries
Requires:       lib%{name} = %{version}-%{release}
Requires:       boost-devel

%description devel
This package provides the header files and C++ driver for MongoDB. MongoDB is
a high-performance, open source, schema-free document-oriented database.

%package server
Summary:        MongoDB server, sharding server and support scripts
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}

%description server
This package provides the mongo server software, mongo sharding server
software, default configuration files, and init scripts.


%prep
%setup -q -n mongodb-src-r%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# spurious permissions
chmod -x README
chmod -x db/repl/rs_exception.h
chmod -x db/resource.h

# wrong end-of-file encoding
sed -i 's/\r//' db/repl/rs_exception.h
sed -i 's/\r//' db/resource.h
sed -i 's/\r//' README

%build
# Disable error on warning, use boost-fs 2
mv SConstruct SConstruct.orig
grep -v 'Werror' SConstruct.orig > SConstruct
sed -i 's/-Wall/-DBOOST_FILESYSTEM_VERSION=2/' SConstruct

scons %{?_smp_mflags} --sharedclient --use-system-all .

%install
rm -rf %{buildroot}
scons install . \
%if "%{dist}" == "el5"
	--extralib termcap \
%endif
	--sharedclient \
	--use-system-all \
	--prefix=%{buildroot}%{_prefix} \
	--nostrip \
	--full
rm -f %{buildroot}%{_libdir}/libmongoclient.a

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

%if 0%{?fedora} >= 15
mkdir -p %{buildroot}/lib/systemd/system
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_libdir}/../lib/tmpfiles.d/mongodb.conf
install -p -D -m 644 %{SOURCE6} %{buildroot}/lib/systemd/system/%{daemon}.service
%else
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initddir}/%{daemon}
%endif
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/mongodb.conf
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{daemon}

mkdir -p %{buildroot}%{_mandir}/man1
cp -p debian/*.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre server
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c "MongoDB Database Server" %{name}
exit 0

%post server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null || :
%else
/sbin/chkconfig --add %{daemon}
%endif


%preun server
if [ $1 = 0 ] ; then
%if 0%{?fedora} >= 15
  /bin/systemctl --no-reload disable %{daemon}.service &> /dev/null
  /bin/systemctl stop %{daemon}.service &> /dev/null
%else
  /sbin/service  stop >/dev/null 2>&1
  /sbin/chkconfig --del %{daemon}
%endif
fi


%postun server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null
%endif
if [ "$1" -ge "1" ] ; then
%if 0%{?fedora} >= 15
   /bin/systemctl try-restart %{daemon}.service &> /dev/null
%else
   /sbin/service %{daemon} condrestart >/dev/null 2>&1 || :
%endif
fi


%files
%defattr(-,root,root,-)
%{_bindir}/mongo
%{_bindir}/mongodump
%{_bindir}/mongoexport
%{_bindir}/mongofiles
%{_bindir}/mongoimport
%{_bindir}/mongorestore
%{_bindir}/mongostat
%{_bindir}/mongosniff
%{_bindir}/bsondump
%{_bindir}/mongotop

%{_mandir}/man1/mongo.1*
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongodump.1*
%{_mandir}/man1/mongoexport.1*
%{_mandir}/man1/mongofiles.1*
%{_mandir}/man1/mongoimport.1*
%{_mandir}/man1/mongosniff.1*
%{_mandir}/man1/mongostat.1*
%{_mandir}/man1/mongorestore.1*
%{_mandir}/man1/bsondump.1*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc README GNU-AGPL-3.0.txt APACHE-2.0.txt
%{_libdir}/libmongoclient.so

%files server
%defattr(-,root,root,-)
%{_bindir}/mongod
%{_bindir}/mongos
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongos.1*
%dir %attr(0755, %{name}, root) %{_sharedstatedir}/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/mongodb.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemon}
%if 0%{?fedora} >= 15
/lib/systemd/system/*.service
%{_libdir}/../lib/tmpfiles.d/mongodb.conf
%else
%{_initddir}/%{daemon}
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/mongo

%changelog
* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-8
- Disable HTTP interface by default (#752331)

* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-7
- Enable journaling by default (#656112)
- Remove BuildRequires on unittest (#755081)

* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-6
- Clean up mongodb-src-r2.0.2-js.patch and fix #787246

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-5
- Enable build using external snappy

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-4
- Patch buildsystem for building on older pythons (RHEL5)

* Mon Jan 16 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-3
- Merge the 2.0.2 spec file with EPEL
- Merge mongodb-sm-pkgconfig.patch into mongodb-src-r2.0.2-js.patch

* Mon Jan 16 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-2
- Add pkg-config enablement patch

* Thu Jan 14 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-1
- Update to 2.0.2
- Add new files (mongotop and bsondump manpage)
- Update mongodb-src-r1.8.2-js.patch => mongodb-src-r2.0.2-js.patch
- Update mongodb-fix-fork.patch
- Fix pcre linking

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Chris Lalancette <clalancette@gmail.com> - 1.8.2-10
- Rebuild for rawhide boost update

* Thu Sep 22 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-9
- Copy the right source file into place for tmpfiles.d

* Tue Sep 20 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-8
- Add a tmpfiles.d file to create the /var/run/mongodb subdirectory

* Mon Sep 12 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-7
- Add a patch to fix the forking to play nice with systemd
- Make the /var/run/mongodb directory owned by mongodb

* Thu Jul 28 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-6
- BZ 725601 - fix the javascript engine to not hang (thanks to Eduardo Habkost)

* Mon Jul 25 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-5
- Fixes to post server, preun server, and postun server to use systemd

* Thu Jul 21 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-4
- Update to use systemd init

* Thu Jul 21 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-3
- Rebuild for boost ABI break

* Wed Jul 13 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-2
- Make mongodb-devel require boost-devel (BZ 703184)

* Fri Jul 01 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-1
- Update to upstream 1.8.2
- Add patch to ignore TERM

* Fri Jul 01 2011 Chris Lalancette <clalance@redhat.com> - 1.8.0-3
- Bump release to build against new boost package

* Sat Mar 19 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-2
- Make mongod bind only to 127.0.0.1 by default

* Sat Mar 19 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-1
- Update to 1.8.0
- Remove upstreamed nonce patch

* Wed Feb 16 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-5
- Add nonce patch

* Sun Feb 13 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-4
- Manually define to use boost-fs v2

* Sat Feb 12 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-3
- Disable extra warnings

* Fri Feb 11 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-2
- Disable compilation errors on warnings

* Fri Feb 11 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-1
- Update to 1.7.5
- Remove CPPFLAGS override
- Added libmongodb package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-3
- Add post/postun ldconfig... oops!

* Mon Dec 06 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-2
- Enable --sharedclient option, remove static lib

* Sat Dec 04 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-1
- New upstream release

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-4
- Put -fPIC onto both the build and install scons calls

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-3
- Define _initddir when it doesn't exist for el5 and others

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-2
- Added -fPIC build option which was dropped by accident

* Thu Oct  7 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.3-1
- removed js Requires
- new upstream release
- added more excludearches: sparc s390, s390x and bugzilla pointer

* Tue Sep  7 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.2-2
- added ExcludeArch for ppc

* Fri Sep  3 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.2-1
- new upstream release 1.6.2
- send mongod the USR1 signal when doing logrotate
- use config options when starting the daemon from the initfile
- removed dbpath patch: rely on config
- added pid directory to config file and created the dir in the spec
- made the init script use options from the config file
- changed logpath in mongodb.conf

* Wed Sep  1 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.1-1
- new upstream release 1.6.1
- patched SConstruct to allow setting cppflags
- stopped using sed and chmod macros

* Fri Aug  6 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.0-1
- new upstream release: 1.6.0
- added -server package
- added new license file to %%docs
- fix spurious permissions and EOF encodings on some files

* Tue Jun 15 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.4.3-2
- added explicit js requirement
- changed some names

* Wed May 26 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.4.3-1
- updated to 1.4.3
- added zlib license for util/md5
- deleted upstream deb/rpm recipes
- made scons not strip binaries
- made naming more consistent in logfile, lockfiles, init scripts etc.
- included manpages and added corresponding license
- added mongodb.conf to sources

* Fri Oct  2 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-3
- fixed libpath issue for 64bit systems

* Thu Oct  1 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-2
- added virtual -static package

* Mon Aug 31 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-1
- Initial release.
