Name:           cln
Version:        1.3.1
Release:        1%{?dist}
Summary:        Class Library for Numbers

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.ginac.de/CLN/
Source0:        http://www.ginac.de/CLN/%{name}-%{version}.tar.bz2
Patch1:         cln-1.3.1-s390x.patch
Patch2:         cln-arm-preprocessor-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires:  gmp-devel
BuildRequires:  texi2html texinfo-tex

%description
A collection of C++ math classes and functions, which are designed for
memory and speed efficiency, and enable type safety and algebraic
syntax.

%package devel
Summary:        Development files for programs using the CLN library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} gmp-devel pkgconfig

%description devel
A collection of C++ math classes and functions, which are designed for
memory and speed efficiency, and enable type safety and algebraic
syntax.

This package is necessary if you wish to develop software based on
the CLN library.

%prep
%setup -q
%patch1 -p0 -b .s390x
%patch2 -p0 -b .fix

%build
%configure --disable-static
make %{?_smp_mflags}
make pdf
make html

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_docdir}/%{name}-devel-%{version}
cp -p doc/cln.pdf doc/cln.html %{buildroot}%{_docdir}/%{name}-devel-%{version}/

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1/pi.*

%check
make %{_smp_mflags} check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info --section="Math" %{_infodir}/cln.info.gz %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/cln.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root)
%doc COPYING NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/cln.pc
%{_includedir}/cln/
%{_infodir}/*.info*
%{_docdir}/%{name}-devel-%{version}

%changelog
* Thu Jul 01 2010 Deji Akingunola <dakingun@gmail.com> - 1.3.1-1
- New upstream version
- build for EPEL6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Deji Akingunola <dakingun@gmail.com> - 1.3.0-1
- Update to latest upstream release 1.3.0

* Thu May 28 2009 Dan Horak <dan[at]danny.cz> - 1.2.2-5
- fix build on s390x
- run the test-suite during build

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 1.2.2-3
- Add upstream patch to build with gcc-4.4

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.2-2
- Bump to solve dependency for ginac-devel

* Tue Apr 29 2008 Quentin Spencer <qspencer@users.sf.net> 1.2.2-1
- Update to 1.2.2.

* Mon Feb 25 2008 Quentin Spencer <qspencer@users.sf.net> 1.2.0-1
- Update to 1.2.0.
- Update License tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.13-5
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Quentin Spencer <qspencer@users.sf.net> 1.1.13-4
- Add pkgconfig as a dependency of -devel.

* Tue Aug 21 2007 Quentin Spencer <qspencer@users.sf.net> 1.1.13-3
- Rebuild for F8.

* Mon Aug 28 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.13-2
- Rebuild for FC-6.

* Thu Aug 17 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.13-1
- New release.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-5
- Disable static build.
- Enable parallel build.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-4
- Rebuild for Fedora Extras 5.
- Remove /usr/share/info/dir after install.
- Exclude static libs.

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-3
- Exclude /usr/share/info/dir from package (bug 178660).

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-2
- Update source URL.

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-1
- New upstream release.

* Mon Oct 31 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.10-1
- New upstream release, incorporating previous patch.

* Mon Jun 20 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-8
- Rebuild

* Mon Jun 13 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-4
- Patched include/cln/string.h to correctly compile on gcc-c++-4.0.0-9

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-3
- Added gmp-devel to Requires for devel

* Fri May 20 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-2
- Added dist tag.

* Wed May 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Excluded .la file

* Fri Apr 22 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Added gmp-devel in BuildRequires, fixes in files
- Added release to name in Requires for devel

* Mon Mar 21 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Adapted spec file for Fedora Extras

* Thu Nov 20 2003 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added pkg-config metadata file to devel package

* Wed Nov  6 2002 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added HTML and DVI docs to devel package

* Tue Nov  5 2001 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added Packager
