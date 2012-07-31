Name: blcr
Version: 0.8.2
Release: 1%{?dist}
Summary: Berkeley Lab Checkpoint/Restart for Linux
Url: http://ftg.lbl.gov/checkpoint
Provides: %{name}-kmod-common = %{version}

# Are we installing the test-suite
%define build_testsuite 1

Group: System Environment/Base
License: GPLv2+
Source: http://ftg.lbl.gov/CheckpointRestart/downloads/%{name}-%{version}.tar.gz
# Patch0 is to prevent enabling service by default
Patch0: blcr-init.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#BuildRequires: chrpath autoconf automake libtool
BuildRequires: chrpath
Requires: /sbin/chkconfig %{name}-kmod >= %{version}
#Generic i386 is NOT supported
ExclusiveArch: i686 x86_64 ppc ppc64 arm

%description
Berkeley Lab Checkpoint/Restart for Linux (BLCR)

This package implements system-level checkpointing of scientific applications
in a manner suitable for implementing preemption, migration and fault recovery
by a batch scheduler.

BLCR includes documented interfaces for a cooperating applications or
libraries to implement extensions to the checkpoint system, such as
consistent checkpointing of distributed MPI applications.
Using this package with an appropriate MPI implementation, the vast majority
of scientific applications which use MPI for communucation on Linux clusters
are checkpointable without any modifications to the application source code.

You must also install the %{name}-libs package and a %{name}-modules_* package
matching your kernel version.
%prep
%setup -q 
%patch0 -p0
#remove some binary junk
rm -f tests/CountingApp.class


%build

# VPATH build required to ensure --enable-multilib will work
mkdir -p builddir
cd builddir
ln -s ../configure .

# Configure the thing
# Order arguments such that user's configure arguments can disable multilib, and
# enable the config-report, but doesn't clobber kernel version info from the
# rpmbuild command line
%configure  \
	--srcdir=.. \
	--enable-testsuite \
	--disable-config-report \
	--with-installed-modules \
	--enable-static \

# Now build it
# Doesn't work with _smp_mflags
make util libcr

%clean
rm -rf ${RPM_BUILD_ROOT}

%install
rm -rf ${RPM_BUILD_ROOT}

cd builddir
make install DESTDIR=${RPM_BUILD_ROOT}
# Install the init script
make -C etc install DESTDIR=${RPM_BUILD_ROOT}

# On some systems rpmbuild dislikes having an RPATH that points
# to a system directory.  Some versions of libtool get this right
# on their own, while others don't.
# So, we try to clean it up here if we have chrpath.
if chrpath --version >& /dev/null; then
chrpath -d ${RPM_BUILD_ROOT}/%{_bindir}/cr_checkpoint
chrpath -d ${RPM_BUILD_ROOT}/%{_bindir}/cr_restart
%if  %{build_testsuite}
  list=`make -C tests --no-print-directory echoval VARNAME=testsexec_PROGRAMS`
  ( cd ${RPM_BUILD_ROOT}/%{_libexecdir}/blcr-testsuite && chrpath -d $list )
%endif
  : # ensure non-empty body
fi

# kill .la files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libcr*.la

%post
if [ $1 = 1 ]; then
  /sbin/chkconfig --add blcr
fi
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/chkconfig --del blcr
fi
exit 0

%files
%defattr(-,root,root,-)
%doc util/license.txt
%doc COPYING
%doc NEWS
%doc doc/README
%doc doc/html
%doc %{_mandir}/man1/cr_checkpoint.1.gz
%doc %{_mandir}/man1/cr_restart.1.gz
%doc %{_mandir}/man1/cr_run.1.gz
%{_bindir}/cr_checkpoint
%{_bindir}/cr_restart
%{_bindir}/cr_run
%{_sysconfdir}/init.d/blcr

#
# Libs in a separate package
#
%package libs
Group: System Environment/Libraries
Summary: Libraries for Berkeley Lab Checkpoint/Restart for Linux
License: LGPLv2+
Requires: /sbin/ldconfig

%description libs
Runtime libraries for Berkeley Lab Checkpoint/Restart for Linux (BLCR)

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc libcr/license.txt
%doc COPYING.LIB
%doc NEWS
%{_libdir}/libcr*.so.0*

#
# Separate -devel package
#
%package devel
Requires: %{name}-libs = %{version}-%{release}
Group: Development/Libraries
Summary: Header and object files for Berkeley Lab Checkpoint/Restart for Linux
License: LGPLv2+

%description devel
Header and object files for Berkeley Lab Checkpoint/Restart for Linux
You must also install the %{name}-libs package.

%files devel
%defattr(-,root,root,-)
%doc libcr/license.txt
%doc COPYING.LIB
%doc README.devel
%{_includedir}/blcr_common.h
%{_includedir}/blcr_errcodes.h
%{_includedir}/blcr_ioctl.h
%{_includedir}/blcr_proc.h
%{_includedir}/libcr.h
# .so files
%{_libdir}/libcr.so
%{_libdir}/libcr_omit.so
%{_libdir}/libcr_run.so

%package static
Requires: %{name}-libs = %{version}-%{release}
Group: Development/Libraries
Summary: Static archive files for Berkeley Lab Checkpoint/Restart for Linux
License: LGPLv2+

%description static
Static archive object files for Berkeley Lab Checkpoint/Restart for Linux
You must also install the %{name}-libs package.

%files static
%defattr(-,root,root,-)
%doc libcr/license.txt
%doc COPYING.LIB
# .a files
%{_libdir}/libcr.a
%{_libdir}/libcr_run.a
%{_libdir}/libcr_omit.a

##
## testsuite as an additional package if configured in
##
%if %{build_testsuite}
%package testsuite
Group: System Environment/Base
Summary: Test suite for Berkeley Lab Checkpoint/Restart for Linux
License: GPLv2+
Requires: %{name} = %{version}
%description testsuite
This package includes tests for Berkeley Lab Checkpoint/Restart for Linux
%files testsuite
%defattr(-,root,root,-)
%doc tests/license.txt
%doc COPYING
%{_libexecdir}/blcr-testsuite
%endif

%changelog
* Sat Apr 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-3
- s/i486/i586/ in ExclusiveArch for F11

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-2
- rebuild for new F11 features

* Fri Jan 16 2009 Neal Becker <ndbecker2@gmail.com> - 0.8.0-1
- Update to 0.8.0 release

* Tue Dec 23 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0-0.2.b5
- Add README.devel to devel pkg

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0-0.1.b5
- Change version/release to comply with packaging reqs
- BR libtool
- Get rid of build_shared, build_static
- BR automake

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-4
- Add static package
- Force autoreconf (for patch1)

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-3
- Test with patch to remove -fno-stack-protector

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-2
- Dont install static libs
- Remove README.devel
- remove CountingApp.class
- Add dist tab

* Thu Dec 18 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-1
- Remove 32-bit lib stuff
- Fix defattr
- Fix buildroot
- Remove paranoid check for i386 build
- Remove build_all_static
- Cleanup static/shared libs stuff.
- Update exclusivearch from upstream
- Fix up doc entries

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0b1-1
- Update to 0.8.0b1

* Sun Nov 30 2008 Neal Becker <ndbecker2@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Fri Jun 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Sat Mar  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.5-1
- Update to 0.6.5
- Kill .la files

* Sat Mar  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-4
- Add BR chrpath

* Sun Feb  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-4
- Fixed building debuginfo

* Sun Feb  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-3
- Add req %%{name}-kmod >= %%{version}
- Don't need to gzip man pages
- Don't strip on install
- Misc cleanups

* Sun Feb  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-2
- Full url for Source

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-1
- Various rpmlint fixes

* Mon Jan 28 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.3-2
- Fix chkconfig to not autostart

