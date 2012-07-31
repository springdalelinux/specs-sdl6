
Name:    xforms
Summary: XForms toolkit library
Version: 1.0.93
Release: 2%{?dist}

License: LGPLv2+
Group:   System Environment/Libraries
#URL:     http://www.nongnu.org/xforms/
URL:     http://xforms-toolkit.org/
#Source0: http://savannah.nongnu.org/download/xforms/xforms-%{version}%{?pre}.tar.gz
#Source1: http://savannah.nongnu.org/download/xforms/xforms-%{version}%{?pre}.tar.gz.sig 
Source0:  http://download.savannah.gnu.org/releases-noredirect/xforms/xforms-%{version}%{?pre}.tar.gz
Source1:  http://download.savannah.gnu.org/releases-noredirect/xforms/xforms-%{version}%{?pre}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libjpeg-devel
%define x_deps xorg-x11-devel libGL-devel
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
BuildRequires: libXpm-devel
# skip xorg-x11-proto-devel, for now, pulled in indirectly via libX11-devel
%define x_deps libGL-devel libX11-devel
%endif
BuildRequires: %{x_deps}

# import/export: png, sgi (optional?)
Requires: netpbm-progs
# import eps,ps (optional?)
#Requires: ghostscript
# eww, http://lists.nongnu.org/archive/html/xforms-development/2010-05/msg00000.html
Requires: xorg-x11-fonts-ISO8859-1-75dpi

%description
XForms is a GUI toolkit based on Xlib for X Window Systems. It
features a rich set of objects, such as buttons, sliders, and menus
etc. integrated into an easy and efficient object/event callback
execution model that allows fast and easy construction of
X-applications. In addition, the library is extensible and new objects
can easily be created and added to the library.

%package devel
Summary: Development files for the XForms toolkit library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{?x_deps}
%description devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?pre}

# rpath hack
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure


%build
%configure \
  --disable-static \
  --enable-optimization="$RPM_OPT_FLAGS"

make %{?_smp_mflags} X_PRE_LIBS=""


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

## Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING.LIB Copyright ChangeLog NEWS README
%{_libdir}/libflimage.so.2*
%{_libdir}/libformsGL.so.2*
%{_libdir}/libforms.so.2*

%files devel
%defattr(-,root,root,-)
%{_bindir}/fd2ps
%{_bindir}/fdesign
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_mandir}/man1/*
%{_mandir}/man5/*


%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.93-1
- xforms-1.0.93

* Tue May 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.93-0.1.pre7
- xforms-1.0.93pre7
- Requires: xorg-x11-fonts-ISO8859-1-75dpi

* Thu Nov 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-2.sp2
- xforms-1.9.92sp2

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-1.sp1
- xforms-1.0.92sp1

* Tue Sep 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-0.4.pre13
- xforms-1.0.92pre13

* Mon Sep 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-0.3.pre12
- xforms-1.0.92pre12

* Wed Sep 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-0.2.pre8
- xforms-1.0.92pre8

* Mon Aug 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.92-0.1.pre7
- xforms-1.0.92pre7

* Mon Aug 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.91-2
- %%files: fix %%defattr typo
- drop libXpm-devel from x_deps

* Mon Jul 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.91-1
- xforms-1.0.91
- nuke rpaths
- rebase prelink/no_undefined patch

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.90-11
- respin (gcc43)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.90-10
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.90-9
- License: LGPLv2+

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-8
- fc6 respin

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-7
- cleanup

* Wed Mar 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-6
- -devel: Req: libjpeg-devel(flimage), libXpm-devel

* Mon Jan 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-5
- prelink.patch: fix undefined symbols in (shared) lib(s)

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-4
- BR: libXpm-devel
- -devel: Req: libX11-devel 

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-3
- BR: libGL-devel
- #BR: libXpm-devel (coming soon)

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-2
- BR: libGL.so.1 -> BR: %%x_pkg-Mesa-libGL 
- remove legacy crud

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-1
- 1.0.90
- new version removes use-of/references-to xmkmf,/usr/X11R6 (#170942)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Nov 23 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.2
- update for Fedora Core support
- remove extraneous macros

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.1
- BuildRequires: libtiff-devel
- add few more %%doc files.

* Fri Apr 02 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.0
- fedora-ize package.

* Mon Jan 20 2003 Rex Dieter <rexdieter at sf.net> 1.0-0
- 1.0-release
- redhat-ize specfile

