Name:           ginac
Version:        1.5.6
Release:        1%{?dist}
Summary:        C++ library for symbolic calculations

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.ginac.de/
Source0:        http://www.ginac.de/%{name}-%{version}.tar.bz2
Patch0:         ginac-1.4.4-ginac_pc_in.patch
Patch1:         ginac-1.5.1-lexer_cpp.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires:  cln-devel >= 1.1 gcc-c++ readline-devel
BuildRequires:  tetex-latex tetex-dvips doxygen transfig
Obsoletes:      GiNaC < 1.3.2
Provides:       GiNaC = %{version}-%{release}

%description
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.


%package devel
Summary: GiNaC development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} cln-devel pkgconfig
Obsoletes: GiNaC-devel < 1.3.2
Provides:  GiNaC-devel = %{version}-%{release}

%description devel
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.

This package contains the libraries, include files and other resources you
use to develop GiNaC applications.


%package utils
Summary: GiNaC-related utilities
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: GiNaC-utils < 1.3.2
Provides:  GiNaC-utils = %{version}-%{release}

%description utils
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.

This package includes ginsh ("GiNaC interactive shell") which provides a
simple and easy-to-use CAS-like interface to GiNaC for non-programmers, and
the tool "viewgar" which displays the contents of GiNaC archives.


%prep
%setup -q

%patch0 -p1 -b .ginac_pc_in
%patch1 -p1 -b .lexer_cpp

%build
%configure --disable-dependency-tracking --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/ginac.info.gz 2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ginac.info.gz 2>/dev/null || :
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_infodir}/*.info*
%{_libdir}/*.so
%{_libdir}/pkgconfig/ginac.pc
%{_includedir}/ginac
%exclude %{_libdir}/*.la

%files utils
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man?/*

%changelog
* Sat Jan 30 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.5.6-1
- Updated to 1.5.6

* Fri Dec 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.5.5-1
- Updated to 1.5.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.1-2
- Rebuild to fix broken deps

* Tue Mar 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.5.1-1
- Patched up lexer.cpp for missing header
- Removed rpaths in pkgconfig file #487612
- Updated to 1.5.1:
-   Added polynomial factorization.
-   New, faster (recursive descent) expression parser.
-   Faster GCD computation.
-   Replaced custom RTTI by standard C++ RTTI.
-   Fixed recursion in polynomial divide that caused a significant slowdown in sqrfree().
-   Improved lsolve() of systems containing non-numeric coefficients.
-   Improved configuration and compatibility.


* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.4.4-1
- Updated to 1.4.4

* Tue Apr 29 2008 Quentin Spencer <qspencer@users.sf.net> 1.4.3-1
- Update to 1.4.3. Remove old patch.

* Sun Mar  2 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1-4
- Patch for building with GCC 4.3 (this has been applied upstream and so
  can be dropped in the next release of ginac).

* Wed Feb 27 2008 Quentin Spencer <qspencer@users.sf.net> 1.4.1-3
- Rebuild for new release of cln.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.1-2
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Quentin Spencer <qspencer@users.sf.net> 1.4.1-1
- Update to 1.4.1.

* Thu Sep 13 2007 Quentin Spencer <qspencer@users.sf.net> 1.4.0-2
- Add pkgconfig as a dependency of -devel.

* Wed Sep 12 2007 Quentin Spencer <qspencer@users.sf.net> 1.4.0-1
- New release. Changes file lists to reflect the removal of some files
  previously in the devel package.

* Tue Aug 21 2007 Quentin Spencer <qspencer@users.sf.net> 1.3.7-1
- New release.

* Wed Jan 10 2007 Quentin Spencer <qspencer@users.sf.net> 1.3.6-1
- New release.

* Mon Aug 28 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.5-1
- New release.

* Fri Apr 14 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.4-1
- New release. Old patch removed.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-4
- Rebuild for Fedora Extras 5.

* Thu Feb  2 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-3
- Patch so it builds on gcc 4.1.
- Disable static libs from build and enable parallel build.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-2
- Exclude /usr/share/info/dir from package.
- New URL.
- Exclude static libs.

* Mon Oct 31 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.3-1
- New upstream release.

* Tue Aug  2 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.2-1
- New upstream release. Changed package name to lowercase letters to
  mirror upstream sources.  Added Provides and Obsoletes for upgrade.

* Sat Jun 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-5
- Added cln-devel as dependency of GiNaC-devel

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-5
- Removed gmp-devel--it should be in cln-devel instead

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-4
- Added gmp-devel to BuildRequires

* Thu May 26 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-3
- Added transfig to BuildRequires

* Thu May 26 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-2
- Added dist tag

* Wed May 18 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-1
- New upstream release.
- Added missing BuildRequires (readline-devel, tetex-*, doxygen).

* Wed May 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-2
- Exclude .la lib.
- Remove processing of info files (this is supposed to be automatic).

* Fri Apr 22 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-2
- Added release to Requires for devel and utils

* Thu Apr 21 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-1
- Adapted spec file for Fedora Extras
- Fixed missing BuildRequires
- Fixed broken install-info command

* Thu Nov 20 2003 Christian Bauer <Christian.Bauer@uni-mainz.de>
- added pkg-config metadata file to devel package

* Thu Nov  1 2001 Christian Bauer <Christian.Bauer@uni-mainz.de>
- moved ginsh and viewgar to "utils" package

* Thu Oct  5 2000 Christian Bauer <Christian.Bauer@uni-mainz.de>
- cleaned up a bit

* Wed Jan 26 2000 Christian Bauer <Christian.Bauer@uni-mainz.de>
- split into user and devel packages

* Wed Dec  1 1999 Christian Bauer <Christian.Bauer@uni-mainz.de>
- aclocal macros get installed
