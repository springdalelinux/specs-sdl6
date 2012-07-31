# This RPM will possibly fail on PowerPCs, but I am ignoring this.
Summary: API in "C" for Shapefile handling
Name: shapelib
Version: 1.3.0b2
Release: 7%{?dist}
# No version of the LGPL is given.
License: LGPLv2+ or MIT
URL: http://shapelib.maptools.org/
Source: http://download.osgeo.org/shapelib/%{name}-%{version}.tar.gz
Patch0: shapelib-1.3.0b1-Makefile.patch
Patch1: shapelib-1.3.0b2-Makefile2.patch
Patch2: shapelib-1.2.10-endian.patch
Patch3: shapelib-1.3.0b1-buildid.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group: Development/Libraries
BuildRequires: proj-devel >= 4.4.1

%package devel
Summary: Development files for shapelib
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%description devel
This package contains libshp and the appropriate header files.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .makefile
%patch1 -p1 -b .makefile2
%patch2 -p1 -b .endian
%patch3 -p1 -b .buildid
sed -i "s/\r//g" README
chmod -x README

%build
make %{?_smp_mflags} libdir=%{_libdir} CFLAGS="$RPM_OPT_FLAGS" lib
make %{?_smp_mflags} libdir=%{_libdir} CFLAGS="$RPM_OPT_FLAGS" all

cd contrib
make %{?_smp_mflags} libdir=%{_libdir} EXTRACFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
find %{buildroot} -name \*\.a -print | xargs rm -f
find %{buildroot} -name \*\.la -print | xargs rm -f

cd contrib
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*

%doc LICENSE.LGPL README README.tree web/*.html
%doc contrib/doc/shpproj.txt stream1.sh stream1.out stream2.sh
%doc stream2.out makeshape.sh stream3.out ChangeLog

%files devel
%defattr(-,root,root,-)
%doc LICENSE.LGPL README
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0b2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 19 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b2-6
- update to latest upstream beta

* Tue Mar 09 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b1-5
- update to latest upstream version

* Fri Feb 19 2010 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-2.20100216cvs
- update patch0-3 fix undefined symbols

* Tue Feb 16 2010 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-1.20100216cvs
- revert to latest cvs snapshot

* Thu Feb 04 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b1-4
- misc cleanups

* Thu Feb 04 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b1-3
- do not package static libfiles (#556094)

* Thu Jan 07 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b1-2
- fix patch2 - no not depend on gdal

* Thu Jan 07 2010 Lucian Langa <cooly@gnome.eu.org> - 1.3.0b1-1
- misc cleanups
- update BR
- fix source0
- update to latest upstream snapshot

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-20.20060304cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-19.20060304cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.10-18.20060304cvs
- fix patch application

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.10-17.20060304cvs
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.10-16.20060304cvs
- Autorebuild for GCC 4.3

* Sun Oct  21 2007 Shawn McCann <mccann0011@hotmail.com> - 1.2.10-15.20060304cvs
- Fix for bug 339931

* Sat Sep  16 2006 Shawn McCann <mccann0011@hotmail.com> - 1.2.10-12.20060304cvs
- Rebuild for FC6

* Sun Mar  5 2006 Shawn McCann <mccann0011@hotmail.com> - 1.2.10-11.20060304cvs
- Fixed a makefile bug that messed up parallel builds

* Sat Mar  4 2006 Shawn McCann <mccann0011@hotmail.com> - 1.2.10-10.20060304cvs
- Upgraded to cvs snapshot taken on March 4, 2006

* Sat Mar  4 2006 Shawn McCann <mccann0011@hotmail.com> - 1.2.10-9
- Rebuild for Fedora Extras 5

* Mon Apr 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.10-8
- Fix "invalid lvalue in assignment" for GCC4.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0:1.2.10-6
- Don't hard-code endianness; just use endian.h

* Wed Dec 15 2004 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:1.2.10-5
- Patched patch and spec file according to suggestions of Michael Schwendt
- In particular, this separates the building from the installing in the rpm.

* Thu Aug 12 2004 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:1.2.10-0.fdr.4
- Moved RPM_OPT_FLAGS out of make files.
- Removed backup files from patch.
- Made sure that make was using the appropriate libdir.

* Mon Dec 22 2003 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:1.2.10-0.fdr.3
- Added url tag, changed copyright to license and changed permissions on patch file.

* Mon Dec 22 2003 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:1.2.10-0.fdr.2
- Add source URL
- Removed proj requirement as it is automatically detected.
- Added epoch to proj-devel requirement
- Fixed post and postun
- Changed group to Development/Libraries, although this appears to be only
  somewhat satisfactory.
- Removed "which make"

* Wed Nov  5 2003 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:1.2.10-0.fdr.1
- Updated to 1.2.10 release
- Major changes to spec for Fedora
- Changes to Makefile patch for Fedora
- Split off devel package
