Name:           ftgl
Version:        2.1.3
Release:        0.3.rc5%{?dist}
Summary:        OpenGL frontend to Freetype 2

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://ftgl.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ftgl/ftgl-%{version}-rc5.tar.bz2
Patch0:         ftgl-2.1.3-rc5-ttf_font.patch
Patch1:         ftgl-2.1.3-rc5-ldflags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen

BuildRequires:  freeglut-devel
BuildRequires:  freetype-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  cppunit-devel

Obsoletes: ftgl-utils < %{version}


%description
FTGL is a free open source library to enable developers to use arbitrary
fonts in their OpenGL (www.opengl.org)  applications.
Unlike other OpenGL font libraries FTGL uses standard font file formats
so doesn't need a preprocessing step to convert the high quality font data
into a lesser quality, proprietary format.
FTGL uses the Freetype (www.freetype.org) font library to open and 'decode'
the fonts. It then takes that output and stores it in a format most 
efficient for OpenGL rendering.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       freetype-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation

%description docs
This package contains documentation files for %{name}.


%prep
%setup -q -n ftgl-%{version}~rc5
%patch0 -p1 -b .destdir
%patch1 -p1 -b .ldflags



%build
%configure \
  --enable-shared \
  --disable-static \
  --with-gl-inc=%{_includedir} \
  --with-gl-lib=%{_libdir} \
  --with-glut-inc=%{_includedir} \
  --with-glut-lib=%{_libdir} \
  --with-x

make all %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __doc
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Doc fixes
mkdir -p __doc/html
install -pm 0644 $RPM_BUILD_ROOT%{_datadir}/doc/ftgl/html/* __doc/html
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/FTGL/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%defattr(-,root,root,-)
%doc __doc/*


%changelog
* Sun Feb 14 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.1.3-0.3.rc5
- Fix Missing ldflags - rhbz#565150

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-0.2.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 kwizart < kwizart at gmail.com > - 2.1.3-0.1.rc5
- Update to 2.1.3-rc5
- Obsoletes -utils sub-package

* Fri Feb 27 2009 kwizart < kwizart at gmail.com > - 2.1.2-10
- Switch from freefont to dejavu-sans-fonts - #480455

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  9 2008 kwizart < kwizart at gmail.com > - 2.1.2-8
- Rebuild for gcc43

* Sat Dec 15 2007 kwizart < kwizart at gmail.com > - 2.1.2-7
- Add -docs to fix multiarch conflicts  #341191
- Fix libGL requirement.
- Project Moved to sourceforge

* Sun Aug 26 2007 kwizart < kwizart at gmail.com > - 2.1.2-6
- rebuild for ppc32
- Update the license field

* Sat Jul 14 2007 kwizart < kwizart at gmail.com > - 2.1.2-5
- Fix version field the whole package

* Fri Jul 13 2007 kwizart < kwizart at gmail.com > - 2.1.2-4
- Modified ftgl-2.1.2-pc_req.patch
- Add Requires freefont to -utils

* Fri Jul 13 2007 kwizart < kwizart at gmail.com > - 2.1.2-3
- Add Requirements for -devel
- Preserve timestramp for install step
- Add ftgl-utils to prevent conflict with multilibs
  Add patch to prevent rpath

* Mon May 28 2007 kwizart < kwizart at gmail.com > - 2.1.2-2
- Add ftgl.pc patch
- Add BR freeglut-devel
- Remove unneeded LDFLAGS
- Cleaned spec file

* Mon May 14 2007 kwizart < kwizart at gmail.com > - 2.1.2-1
- Initial package for Fedora
