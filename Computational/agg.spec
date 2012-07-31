Summary: Anti-Grain Geometry graphical rendering engine
Name:    agg
Version: 2.5
Release: 9%{?dist}
Group:   System Environment/Libraries
URL:     http://www.antigrain.com
License: GPLv2+
#Source0:  http://www.antigrain.com/%{name}-%{version}.tar.gz
Source0: %{name}-free-%{version}.tar.gz
# agg contains gpc.c, 'free for non-commercial use', we cannot ship.
# We use this script to remove the non-free code before shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# sh agg-generate-tarball.sh 2.5
Source1: agg-generate-tarball.sh

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: automake, libtool, libX11-devel, freetype-devel, SDL-devel

Patch0: agg-2.4-depends.patch
Patch1: agg-2.5-pkgconfig.patch

%description
A High Quality Rendering Engine for C++.

%package devel
Summary: Support files necessary to compile applications with agg
Group: Development/Libraries
Requires: agg = %{version}-%{release}, freetype-devel
# for _datadir/automake ownership
Requires: automake

%description devel
Libraries, headers, and support files necessary to compile applications 
using agg.

%prep
%setup -q
%patch0 -p1 -b .depends
%patch1 -p1 -b .pkgconfig
aclocal
autoheader
autoconf
libtoolize --force
automake --foreign --add-missing --ignore-deps

%build
%configure --disable-static --disable-gpc
# parallel build fails in examples/ because the .la is in _LDFLAGS instead of
# _LIBADD
make #%%{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/*.la

rm -rf __dist_examples __clean_examples
cp -a examples __clean_examples
make -C __clean_examples distclean
rm -rf __clean_examples/Makefile.am __clean_examples/{win32*,macosx*,BeOS}
mkdir __dist_examples
mv __clean_examples __dist_examples/examples

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc authors copying readme news
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc __dist_examples/examples
%{_libdir}/*.so
%{_libdir}/pkgconfig/libagg.pc
%{_includedir}/agg2/
%{_datadir}/aclocal/libagg.m4

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jan 29 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.5-9
- also remove include/agg_conv_gpc.h as it also carries a copy of the non-Free
  GPC license (upstream also recommends removing that file under
  http://www.antigrain.com/license/index.html#toc0005) (#559611)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Patrice Dumas <pertusus@free.fr> - 2.5-6
- remove non free files
- minor cleanups
- parallel build fails

* Fri Aug 03 2007 Caolan McNamara <caolanm@redhat.com> - 2.5-4
- clarify license
- source upstream silently changed even though version remained
  unchanged

* Tue Jun 26 2007 Caolan McNamara <caolanm@redhat.com> - 2.5-3
- Resolves: rhbz#245650 -devel Require: freetype-devel

* Mon Apr 23 2007 Caolan McNamara <caolanm@redhat.com> - 2.5-2
- Resolves: rhbz#237493 misapplied patch

* Sat Jan 06 2007 Caolan McNamara <caolanm@redhat.com> - 2.5-1
- bump to 2.5

* Fri Nov 10 2006 Caolan McNamara <caolanm@redhat.com> - 2.4-3
- Resolves: rhbz#214970 rebuild with new 2.4 sources

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4-2.1
- rebuild

* Mon Jul 10 2006 Caolan McNamara <caolanm@redhat.com> - 2.4-2
- rh#198174# add extra links from libs to their runtime requirements

* Wed May 10 2006 Caolan McNamara <caolanm@redhat.com> - 2.4-1
- next version

* Fri Feb 17 2006 Karsten Hopp <karsten@redhat.de> 2.3-4
- add BuildRequires freetype-devel for ft2build.h

* Mon Feb 13 2006 Caolan McNamara <caolanm@redhat.com> - 2.3-3
- BuildRequires

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3-2.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Caolan McNamara <caolanm@redhat.com> - 2.3-2
- rh#180341# BuildRequires

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Nov 23 2005 Caolan McNamara <caolanm@redhat.com> 2.3-1
- initial import
