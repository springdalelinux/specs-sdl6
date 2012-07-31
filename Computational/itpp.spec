Name:           itpp
Version:        4.0.6
Release:        2%{?dist}
Summary:        C++ library for math, signal/speech processing, and communications

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://itpp.sourceforge.net/
Source0:        http://downloads.sourceforge.net/itpp/itpp-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Filed into upstream bugtracker at:
# https://sourceforge.net/tracker/?func=detail&aid=2780001&group_id=37044&atid=418758
Patch1:			itpp-gcc44.patch

BuildRequires:  gcc-gfortran, atlas-devel, fftw-devel
BuildRequires:  tetex-latex
BuildRequires:  doxygen, ghostscript

%description
IT++ is a C++ library of mathematical, signal processing, speech
processing, and communications classes and functions.  The kernel of
the IT++ library is built upon templated vector and matrix classes
with many functions for their manipulation.  Such a kernel makes IT++
similar to Octave.  IT++ makes extensive use of existing open-source
libraries (but not only) for increased functionality, speed, and
accuracy.


%package devel
Summary:        Development files for itpp
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       fftw-devel, atlas-devel, gcc-gfortran

%description devel
This package contains the itpp header files, libs, and man pages.


%package doc
Summary:        Documentation for itpp
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains the documentation for itpp.


%prep
%setup -q
%patch1 -b .gcc44

%build
export LDFLAGS="-L"%{_libdir}"/atlas"
export CPPFLAGS="-I/usr/include/atlas"
export F77=gfortran
%configure --with-blas="-latlas -lblas" --disable-dependency-tracking  \
  --with-docdir=%{_docdir}/%{name}-%{version} --disable-static
make -k %{?_smp_mflags}
#
#  remove unnecessary bits from itpp-config and itpp.pc
#cat itpp-config | sed -e 's|-L[^ ]*gcc[^ ]*||g' |  \
#    sed -e 's|-I[^ ]*||g' > itpp-config_new
#mv -f itpp-config_new itpp-config
#cat itpp.pc | sed -e 's|-L[^ ]*gcc[^ ]*||g' |  \
#    sed -e 's|-I[^ ]*||g' > itpp.pc_new
#mv -f itpp.pc_new itpp.pc


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
cp -p COPYING AUTHORS ChangeLog NEWS README \
  $RPM_BUILD_ROOT/%{_docdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/[A-Z]*
%{_libdir}/*.so.*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_bindir}/%{name}-config
%{_mandir}/man1/*

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/html


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 4.0.6-1
- Fix FTBFS:
- Update to 4.0.6 bugfix release
- Dropped itpp-gcc43.patch (merged upstream).
- Added itpp-gcc44.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 4.0.0-6
- Rebuild for atlas-3.8.2

* Sun Sep 14 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 4.0.0-5
- Fix building with gcc4.3

* Fri May 23 2008 Jon Stanley <jonstanley@gmail.com> - 4.0.0-4
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.0.0-3
- Autorebuild for GCC 4.3

* Sun Dec  9 2007  Ed Hill <ed@eh3.com> - 4.0.0-2
- fix hard-coded libdir error

* Sun Dec  9 2007  Ed Hill <ed@eh3.com> - 4.0.0-1
- new upstream 4.0.0

* Sat Aug 25 2007  Ed Hill <ed@eh3.com> - 3.10.12-1
- new upstream 3.10.12

* Tue Apr 17 2007  Ed Hill <ed@eh3.com> - 3.10.10-1
- new upstream 3.10.10

* Tue Apr 17 2007  Ed Hill <ed@eh3.com> - 3.10.9-2
- fix dir ownership per bz #233842

* Sun Mar 18 2007  Ed Hill <ed@eh3.com> - 3.10.9-1
- new upstream 3.10.9

* Sat Feb 10 2007  Ed Hill <ed@eh3.com> - 3.10.8-1
- new upstream 3.10.8

* Wed Dec  6 2006  Ed Hill <ed@eh3.com> - 3.10.7-1
- new upstream 3.10.7

* Sun Oct 28 2006  Ed Hill <ed@eh3.com> - 3.10.6-1
- new upstream 3.10.6

* Wed Oct 11 2006  Ed Hill <ed@eh3.com> - 3.10.5-7
- explicitly link with -lstdc++

* Tue Oct 10 2006  Ed Hill <ed@eh3.com> - 3.10.5-6
- fix unowned dir

* Sun Oct  8 2006  Ed Hill <ed@eh3.com> - 3.10.5-5
- fix permissions for itpp/base/itpp_version.h
- make sure we ship the license
- remove redundant BRs and add -devel BRs
- remove only the gcc bits from itpp-config and itpp.pc

* Sat Oct  7 2006  Ed Hill <ed@eh3.com> - 3.10.5-4
- disable dependency tracking to speed build, sanitize itpp.pc,
  and de-macro-ize an earlier changelog entry

* Sat Sep 23 2006  Ed Hill <ed@eh3.com> - 3.10.5-3
- disable static libs, add pkgconfig, and sanitize itpp-config

* Tue Sep 13 2006  Ed Hill <ed@eh3.com> - 3.10.5-2
- fix the html docs and add BuildRequires

* Tue Sep 12 2006  Ed Hill <ed@eh3.com> - 3.10.5-1
- initial version for Fedora Extras

* Mon Feb 13 2006  Adam Piatyszek  <ediap@users.sourceforge.net>
- Created subpackage `itpp-html-doc' with HTML documentation

* Fri Feb 10 2006  Adam Piatyszek  <ediap@users.sourceforge.net>
- Added missing *.a and *.m files

* Thu Feb 09 2006  Adam Piatyszek  <ediap@users.sourceforge.net>
- Changes in `Name', `Version' and `Release' definitions
- Removed distribution dependent release settings
- Added DESTDIR to make install command

* Wed Dec 28 2005  Adam Piatyszek  <ediap@users.sourceforge.net>
- Fixed `name' and `version' definitions
- Added `itpp-config' in files section

* Fri Dec 23 2005  Adam Piatyszek  <ediap@users.sourceforge.net>
- Initial spec file prepared
