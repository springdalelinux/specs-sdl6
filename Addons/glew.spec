Name:           glew
Version:        1.5.5
Release:        1%{?dist}
Summary:        The OpenGL Extension Wrangler Library
Group:          System Environment/Libraries
License:        BSD and MIT
URL:            http://glew.sourceforge.net

Source0:	http://downloads.sourceforge.net/project/glew/glew/%{version}/glew-%{version}.tgz
Patch0:         glew-1.5.2-makefile.patch
Patch1:		glew-1.5.2-add-needed.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libGLU-devel

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++
extension loading library. GLEW provides efficient run-time mechanisms for
determining which OpenGL extensions are supported on the target platform.
OpenGL core and extension functionality is exposed in a single header file.
GLEW is available for a variety of operating systems, including Windows, Linux,
Mac OS X, FreeBSD, Irix, and Solaris.


%package devel
Summary:        Development files for glew
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGLU-devel

%description devel
Development files for glew


%prep
%setup -q
%patch0 -p1 -b .make
%patch1 -p1 -b .add

sed -i -e 's/\r//g' config/config.guess

%build

make %{?_smp_mflags} CFLAGS.EXTRA="$RPM_OPT_FLAGS" includedir=%{_includedir} GLEW_DEST= libdir=%{_libdir} bindir=%{_bindir}


%install
rm -rf $RPM_BUILD_ROOT
make install GLEW_DEST="$RPM_BUILD_ROOT" libdir=%{_libdir} bindir=%{_bindir} \
  includedir=%{_includedir}
rm $RPM_BUILD_ROOT%{_libdir}/libGLEW.a


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_bindir}/*
%{_libdir}/libGLEW.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libGLEW.so
%{_libdir}/pkgconfig/glew.pc
%{_includedir}/GL/*.h
%doc doc/*

%changelog
* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.5.5-1
- glew 1.5.5

* Fri Jul 30 2010 Dave Airlie <airlied@redhat.com> 1.5.4-2
- fix glew.pc file as pointed out by David Aguilar

* Sat May 29 2010 Dave Airlie <airlied@redhat.com> 1.5.4-1
- glew 1.5.4 - add glew.pc

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.5.2-2
- glew-1.5.2-add-needed.patch: Fix FTBFS from --no-add-needed

* Tue Feb 02 2010 Adam Jackson <ajax@redhat.com> 1.5.2-1
- glew 1.5.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Jochen Schmitt <Jochen herr-schmitt de> - 1.5.1-1
- New upstream release (#469639)
- Fix licenseing issue with developer documentation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5.0-1
- New upstream version, now SGI licensed stuff free out of the box!
- Unfortunately some of the included docs are under a non free license,
  therefor this package is based on a modified tarbal with these files removed

* Sat Jan 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-4
- Add missing GL_FLOAT_MATXxX defines

* Sat Aug 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-3
- Fix multiple unused direct shlib dependencies in libGLEW.so
- Remove the "SGI Free Software License B" and "GLX Public License" tekst from
  the doc dir in the tarbal
- Patch credits.html to no longer refer to the 2 non free licenses, instead it
  now points to LICENSE-README.fedora
- Put API docs in -devel instead of main package

* Mon Aug  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-2
- Remove SGI encumbered files to make this ok to go into Fedora
- Replace some removed files with (modified) mesa files
- Regenerate some of the removed files using the mesa replacemenmt files
  and the scripts in the auto directory
- Readd wglew.h, some programs may need this to compile
- Update License tag for new Licensing Guidelines compliance

* Sun May 06 2007 Ian Chapman <packages@amiga-hardware.com> 1.4.0-1%{?dist}
- Updated to 1.4.0

* Sun Mar 04 2007 Ian Chapman <packages@amiga-hardware.com> 1.3.6-1%{?dist}
- Updated to 1.3.6
- Updated pathandstrip patch
- Dropped xlib patch - fixed upstream
- Dropped sed EOL replacements - fixed upstream
- Changed license to GPL

* Fri Dec 01 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.5-1%{?dist}
- Updated to 1.3.5
- Fixed stripping of the binaries
- Reinstate parallel building, no longer appears broken
- Removed FC4 specifics from spec (no longer supported)

* Tue Jun 20 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-3%{?dist}
- Added buildrequire macros to determine fc4, fc5, fc6 due to X modularisation

* Sun Jun 04 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-2%{?dist}
- Replaced %%{_sed} macro with sed
- Replaced xorg-x11-devel (build)requires with libGLU-devel for compatibility
  with modular / non-modular X
- Replaced source URL to use primary sf site rather than a mirror
- Removed superfluous docs from devel package
- Removed wglew.h, seems to be only useful for windows platforms

* Thu May 11 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-1.iss
- Initial Release
