Name:           libass
Version:        0.10.0
Release:        1%{?dist}
Summary:        Portable library for SSA/ASS subtitles rendering

Group:          System Environment/Libraries
License:        ISC
URL:            http://code.google.com/p/libass/
Source0:        http://libass.googlecode.com/files/%{name}-%{version}.tar.xz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libpng-devel
BuildRequires:  enca-devel
BuildRequires:  fontconfig-devel
BuildRequires:  fribidi-devel


%description
Libass is a portable library for SSA/ASS subtitles rendering.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Changelog COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libass.pc

%changelog
* Wed Nov 11 2011 Martin Sourada <mso@fedoraproject.org> - 0.10.0-1
- New upstream release
  - various improvements and fixes
- BuildRequires: fribidi-devel (bidirectional text suport)
- Fixes some wierd memory allocation related crash with freetype 2.4.6
  - rhbz 753017, rhbz 753065

* Tue May 31 2011 Martin Sourada <mso@fedoraproject.org> - 0.9.12-1
- New upstream release
  - Licence changed to ISC
  - Fixed word-wrapping
  - Improved charmap fallback matching
  - Various other improvements and fixes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.11-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.11-1
- Fixes rhbz #630432
- New upstream release
  - Various fixes
  - Performance improvements
  - Calculate drawing bounding box like VSFilter
  - Better PAR correction if text transforms are used
  - Improved fullname font matching
  - Add ass_flush_events API function
  - Basic support for @font vertical text layout

* Fri Jul 30 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.9-1
- Fixes rhbz #618733
- New upstream release
  - Parse numbers in a locale-independent way
  - Disable script file size limit
  - Match fonts against the full name ("name for humans")
  - Reset clip mode after \iclip
  - Improve VSFilter compatibility
  - A couple of smaller fixes and cleanups

* Sun Jan 10 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.8-2
- Fix source URL

* Sun Oct 25 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.8-1
- New upstream release
- See http://repo.or.cz/w/libass.git?a=blob;f=Changelog for changes

* Mon Aug 10 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.7-1
- New upstream release
- Upstream changed from sourceforge to code.google

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2008 Martin Sourada <mso@fedoraproject.org> - 0.9.6-2
- remove glibc-devel and freetype-devel BRs, they're already pulled in by the
  rest

* Sun Mar 22 2008 Martin Sourada <mso@fedoraproject.org> - 0.9.6-1
- update to newever version
- drop %%doc from -devel
- update source url to conform with fedora packaging guidelines

* Sun Mar 22 2008 Martin Sourada <mso@fedoraproject.org> - 0.9.5-1
- Initial rpm package
