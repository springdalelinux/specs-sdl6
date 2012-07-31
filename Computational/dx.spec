Summary: Open source version of IBM's Visualization Data Explorer
Name: dx
Version: 4.4.4
Release: 18%{?dist}
URL: http://www.opendx.org/
Group: Applications/Engineering
Source0: http://opendx.informatics.jax.org/source/dx-%{version}.tar.gz
Source1: %{name}.desktop
Patch0: %{name}-rpm.patch
Patch1: %{name}-open.patch
Patch2: %{name}-gcc43.patch
# fixes http://www.opendx.org/bugs/view.php?id=236
Patch3: %{name}-errno.patch
# fix NULL pointer dereference when running dxexec over ssh
# without X forwarding
Patch4: %{name}-null.patch
# remove calls to non-public ImageMagick function to fix linking
Patch5: %{name}-magick.patch
License: IBM
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: bison
BuildRequires: desktop-file-utils
BuildRequires: flex
BuildRequires: hdf-static, hdf-devel
BuildRequires: ImageMagick-devel
#FIXME doesn't build currently
#BuildRequires: java-devel
BuildRequires: lesstif-devel
BuildRequires: libGL-devel
BuildRequires: libGLU-devel
BuildRequires: libtool
BuildRequires: libXinerama-devel
BuildRequires: libXpm-devel
BuildRequires: netcdf-devel
BuildRequires: openssh-clients
Requires: openssh-clients

%description
OpenDX is a uniquely powerful, full-featured software package for the
visualization of scientific, engineering and analytical data: Its open
system design is built on familiar standard interface environments. And its
sophisticated data model provides users with great flexibility in creating
visualizations.

%package libs
Summary: OpenDX shared libraries
Group: System Environment/Libraries
Obsoletes: %{name} < 4.4.4-5

%description libs
This package contains the shared libraries from OpenDX.

%package devel
Summary: OpenDX module development headers and libraries
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
If you want to write a module to use in the Data Explorer Visual Program
Editor, or in the scripting language, you will need this package.

%prep
%setup -q
%patch0 -p1 -b .r
%patch1 -p1 -b .open
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .errno
%patch4 -p1 -b .null
%patch5 -p1 -b .magick
# fix debuginfo rpmlint warnings
chmod a-x src/exec/{dxmods,dpexec,hwrender}/*.{c,h}

%build
autoreconf --force --install
%configure \
	--disable-static \
	--enable-shared \
	--with-jni-path=%{java_home}/include \
	--without-javadx \
	--disable-dependency-tracking \
	--enable-smp-linux \
	--enable-new-keylayout \
	--with-rsh=%{_bindir}/ssh

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

ln -s ../../%{_lib}/dx/bin_linux $RPM_BUILD_ROOT%{_datadir}/dx/

mv $RPM_BUILD_ROOT%{_libdir}/arch.mak $RPM_BUILD_ROOT%{_includedir}/dx/

install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
sed -e 's/"R. c #b4b4b4",/"R. c none",/' src/uipp/ui/icon50.xpm > $RPM_BUILD_ROOT%{_datadir}/pixmaps/dx.xpm
desktop-file-install --vendor fedora \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
	%{SOURCE1}

# cleanup buildroot
rm -rf $RPM_BUILD_ROOT%{_datadir}/dx/doc
rm     $RPM_BUILD_ROOT%{_datadir}/dx/lib/outboard.c
rm     $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog LICENSE NEWS doc/README*
%{_bindir}/*
%{_libdir}/dx
%{_datadir}/dx
%{_mandir}/*/*
%{_datadir}/pixmaps/*.xpm
%{_datadir}/applications/*.desktop

%files libs
%defattr(644,root,root,755)
%{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/dx
%{_includedir}/*.h
%{_libdir}/lib*.so

%changelog
* Wed Sep 29 2010 jkeating - 4.4.4-18
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 4.4.4-17
- rebuild against new ImageMagick

* Sun Mar 07 2010 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-16
- rebuild against latest ImageMagick

* Sat Feb 27 2010 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-15
- fix netcdf detection (headers are back in /usr/include),
  drop unnecessary patch hunk (rhbz #569066)

* Fri Feb 26 2010 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-14
- fix FTBFS due to calls to non-public function from ImageMagick

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 4.4.4-13
- Explicitly BR hdf-static in accordance with the Packaging
  Guidelines (hdf-devel is still static-only).

* Sun Nov 08 2009 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-12
- bump release to clear up cvs tag mixup

* Thu Nov 05 2009 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-11
- updated source URL
- fix build afainst new netcdf headers location
- fix build against new ImageMagick
- fix NULL pointer dereference when running dxexec over ssh
  without X forwarding

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-8
- fix leftover dxexec process consuming 100% CPU after quitting (bug #469664)
- fix building with current libtool/autoconf

* Wed Sep 24 2008 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-7
- rediff patch to fix build with new rpm

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.4.4-6
- Autorebuild for GCC 4.3

* Mon Jan 07 2008 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-5
- fix build with gcc-4.3
- drop X-Fedora from desktop file (per current packaging guidelines)
- move shared libraries to a subpackage to avoid multilib conflicts
  (bug #341041)

* Fri Aug 17 2007 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-4
- fix open() invocation with O_CREAT and no mode
- update License: in accordance with latest guidelines

* Wed Jul 04 2007 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-3
- rebuild against new netcdf shared libs
- fix menu icon transparency (#207841)
- drop redundant BRs
- fix some rpmlint warnings

* Wed Sep 27 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-2
- rebuild against lesstif

* Fri Sep 22 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-1
- updated to 4.4.4

* Sun Sep 17 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-5
- fix make -jN build

* Sun Sep 03 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-4
- moved arch.mak to _includedir/dx
- fixed program startup from the main ui

* Sat Sep 02 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-3
- removed -samples, will package separately
- disable java parts completely for now
- fixed build on fc6
- moved non-binary stuff to _datadir

* Tue Aug 29 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-2
- simplified autotools invocation
- added dist tag

* Tue Aug 22 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-1
- renamed to dx
- package samples
- install desktop file and icon
- use ssh instead of rsh
- run ldconfig for libs

* Sat Aug 19 2006 Dominik Mierzejewski <rpm@greysector.net>
- fixed remaining paths
- split off -devel package
- added missing BRs
- smp_mflags work again
- TODO: java parts

* Fri Aug 18 2006 Dominik Mierzejewski <rpm@greysector.net>
- initial build
- fix lib paths
