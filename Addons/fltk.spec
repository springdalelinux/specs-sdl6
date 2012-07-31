
%global arch %(arch 2>/dev/null || echo undefined)

Summary:	C++ user interface toolkit
Name:		fltk
Version:	1.1.10
Release:	1%{?dist}

# see COPYING (or http://www.fltk.org/COPYING.php ) for exceptions details
License:	LGPLv2+ with exceptions	
Group:		System Environment/Libraries
URL:		http://www.fltk.org/
%if "%{?snap:1}" == "1"
Source0:        http://ftp.easysw.com/pub/fltk/snapshots/fltk-1.1.x-%{snap}.tar.bz2
%else
Source0:        http://ftp.easysw.com/pub/fltk/%{version}%{?pre}/%{name}-%{version}%{?pre}-source.tar.bz2
#Source0:         http://ftp.rz.tu-bs.de/pub/mirror/ftp.easysw.com/ftp/pub/fltk/1.1.10rc3/fltk-1.1.10rc3-source.tar.bz2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: fltk-config.sh

## FIXME/TODO: upstream these asap -- Rex
Patch1:        	fltk-1.1.9-fltk_config.patch 
Patch2:         fltk-1.1.9-test.patch
# libfltk_gl.so had undefined symbols
Patch3: 	fltk-1.1.x-r5750-undefined.patch
# nuke --rpath (#238284)
Patch4: 	fltk-1.1.9-rpath.patch
Patch5: 	fltk-1.1.8-fluid_desktop.patch
Patch7:         fltk-1.1.9-scandir.patch
# use output of `pkg-config xft --libs` instead of just -lXft
Patch8: 	fltk-1.1.10-pkgconfig_xft.patch

%if 0%{?rhel} > 4 || 0%{?fedora} > 4
BuildRequires:  libICE-devel libSM-devel
BuildRequires:	libXext-devel libXinerama-devel libXft-devel libXt-devel libX11-devel
BuildRequires:  xorg-x11-proto-devel xorg-x11-utils
%else
BuildRequires:  xorg-x11-devel
%endif
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libGL-devel libGLU-devel 
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:	man

%description
FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit.
It provides modern GUI functionality without the bloat, and supports
3D graphics via OpenGL and its built-in GLUT emulation.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:       libGL-devel libGLU-devel
%if 0%{?rhel} > 4 || 0%{?fedora} > 4
Requires:       libXft-devel libXext-devel
Requires:       libX11-devel libSM-devel libICE-devel
%else
Requires:       xorg-x11-devel
%endif
%description devel
%{summary}.

%package static
Summary:  Static libraries for %{name}
Group:    Development/Libraries	
Requires: %{name}-devel = %{version}-%{release}
%description static
%{summary}.

%package fluid
Summary:	Fast Light User Interface Designer
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}
%description fluid
%{summary}, an interactive GUI designer for %{name}. 


%prep
%if "%{?snap:1}" == "1"
%setup -q -n fltk-1.1.x-%{snap}
%else
%setup -q  -n fltk-%{version}%{?pre}
%endif

%patch1 -p1 -b .fltk_config
%patch2 -p1 -b .test
%patch3 -p1 -b .undefined
%patch4 -p1 -b .rpath
%patch5 -p1 -b .fluid_desktop
# FIXME, why only needed for F-11+/gcc44 ?
%if 0%{?fedora} > 10
%patch7 -p1 -b .gcc44
%endif
%patch8 -p1 -b .pkgconfig_xft


%build

# using --with-optim, so unset CFLAGS/CXXFLAGS
export CFLAGS=" "
export CXXFLAGS=" "

%configure \
  --with-optim="%{optflags}" \
  --enable-largefile \
  --enable-shared \
  --enable-threads \
  --enable-xdbe \
  --enable-xinerama \
  --enable-xft

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 

# Makefile hack for 64bitness
%if "%{_lib}" != "lib"
mkdir -p $RPM_BUILD_ROOT%{_libdir}
pushd $RPM_BUILD_ROOT%{_libdir}/..
ln -s %{_lib} lib
popd
%endif

make install install-desktop DESTDIR=$RPM_BUILD_ROOT 

# omit examples/games: 
make -C test uninstall-linux DESTDIR=$RPM_BUILD_ROOT
rm -f  $RPM_BUILD_ROOT%{_mandir}/man?/{blocks,checkers,sudoku}*

# Makefile hack for 64bitness
%if "%{_lib}" != "lib"
rm -f  $RPM_BUILD_ROOT%{_libdir}/../lib
%endif

# hack to make fltk-config multilib-safe
mv $RPM_BUILD_ROOT%{_bindir}/fltk-config \
   $RPM_BUILD_ROOT%{_bindir}/fltk-config-%{arch}
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fltk-config

# docs
rm -rf __docs
mv $RPM_BUILD_ROOT%{_docdir}/fltk __docs

## unpackaged files
# errant docs
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat*


%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/fluid.desktop
make -C test 


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post fluid
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun fluid
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans fluid
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files
%defattr(-,root,root,-)
%doc ANNOUNCEMENT CHANGES COPYING CREDITS README
%{_libdir}/libfltk.so.1.1
%{_libdir}/libfltk_forms.so.1.1
%{_libdir}/libfltk_gl.so.1.1
%{_libdir}/libfltk_images.so.1.1

%files devel
%defattr(-,root,root,-)
%doc __docs/*
# fltk-config multilib-safe wrapper
%{_bindir}/fltk-config
%{_bindir}/fltk-config-%{arch}
%{_includedir}/FL/
%{_includedir}/Fl
%{_libdir}/libfltk.so
%{_libdir}/libfltk_forms.so
%{_libdir}/libfltk_gl.so
%{_libdir}/libfltk_images.so
%{_mandir}/man1/fltk-config.1*
%{_mandir}/man3/fltk.3*

%files static
%defattr(-,root,root,-)
%{_libdir}/libfltk.a
%{_libdir}/libfltk_forms.a
%{_libdir}/libfltk_gl.a
%{_libdir}/libfltk_images.a

%files fluid
%defattr(-,root,root,-)
%{_bindir}/fluid
%{_mandir}/man1/fluid.1*
%{_datadir}/applications/fluid.desktop
%{_datadir}/icons/hicolor/*/*/*
# FIXME, add according to new mime spec
%{_datadir}/mimelnk/*/*.desktop


%changelog
* Sun Feb 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.10-1
- fltk-1.1.10
- FTBFS fltk-1.1.10-0.1.rc3.fc13: ImplicitDSOLinking (#564877)

* Tue Dec 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.10-0.1.rc3
- fltk-1.1.10rc3

* Mon Dec 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.9-7
- real -static subpkg (#545145)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.9-5
- fltk-fluid duplicate .desktop file (#508553)
- optimize scriptlets

* Wed May 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.9-4
- unbreak fltk-config --ldstaticflags (#500201)
- (another?) gcc44 patch
- -devel: +Provides: %%name-static
- fix multiarch conflicts (#341141)

* Wed Mar 04 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.9-3
- fix uses of strchr wrt. constness

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.9-1
- fltk-1.1.9

* Sat Mar 29 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-1
- fltk-1.1.8 (final)

* Tue Feb 29 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-0.8.r6027
- fltk-1.1.x-r6027

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-0.7.r5989 
- respin (gcc43)

* Wed Dec 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.6.r5989
- --enable-largefile
- fltk-1.1.x-r5989 snapshot (1.1.8 pre-release)

* Mon Aug 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.5.r5750
- License: LGPLv2+ with exceptions

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.4.r5750
- License: LGPLv2+ (with exceptions)

* Sun Apr 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.3.r5750
- *really* fix --rpath issue, using non-empty patch this time (#238284)

* Sun Apr 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.2.r5750
- nuke --rpath (#238284)

* Thu Apr 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.8-0.1.r5750
- fltk-1.1.x-r5750 snapshot (1.1.8 pre-release)
- --enable-xinerama
- patch for undefined symbols in libfltk_gl

* Wed Apr  4 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.1.7-9.r5555
- Always apply fltk-config patch (#199656)
- Update fltk-1.1.7-config.patch

* Wed Dec 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-8.r5555
- more 64bit hackage to workaround broken Makefile logic (#219348)

* Wed Dec 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-7.r5555
- fltk-1.1.x-r5555 snapshot, for 64bit issues (#219348)
- restore static libs (they're tightly coupled with fltk-config)
- cleanup %%description's

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-6
- move tests to %%check section

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-5
- use included icon/.desktop files
- fix up fltk-config (#199656)

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-3
- follow icon spec
- omit static libs

* Wed Sep 06 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1.1.7-2
- rebuild for FC6

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.7-1
- Upstream update

* Thu Nov 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-4
- Fixed BR and -devel Requires for modular X

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-3
- Update BuildRequires as well

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-2
- Update Requires for -devel

* Thu Oct 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-1
- Upstream update

* Thu Aug 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.4-10
- Fixed BR/Requires for x86_64

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.8
- Hopefully fixed Xft flags for rh80

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.7
- Fixed typo

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.6
- Added xft.pc build dependency
- Added BuildReq:man

* Sun Nov  9 2003 Ville Skyttä <ville.skytta@iki.fi> 0:1.1.4-0.fdr.4
- Spec file cleanup
- Enabled xft and threads

* Tue Oct 28 2003 Dams <anvil[AT]livna.org> - 0:1.1.4-0.fdr.3
- Added missing symlink in includedir

* Wed Oct  1 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.2
- Removed comment after scriptlets

* Wed Oct  1 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.1
- Updated to final 1.1.4

* Wed Sep 24 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.4.rc1
- Fixed documentation path in configure

* Fri Aug 29 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.3.rc1
- Fixed typo in desktop entry
- Added missing BuildRequires ImageMagick and desktop-file-utils

* Fri Aug 29 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.2.rc1
- Moved fluid to its own package
- Added missing Requires for devel package

* Sat Aug 16 2003 Dams <anvil[AT]livna.org>
- Initial build.
