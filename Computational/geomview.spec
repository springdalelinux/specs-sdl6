
# make -libs subpkg
%define libs 1

Name:    geomview
Summary: Interactive 3D viewing program
Version: 1.9.4
Release: 10%{?dist}

License: LGPLv2+
Url:     http://www.geomview.org/
Group:   Applications/Engineering
Source0: http://dl.sourceforge.net/sourceforge/geomview/geomview-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# http://bugzilla.redhat.com/bugzilla/182625
#ExcludeArch: x86_64

# app.desktop
Source1: geomview.desktop
# mime
Source10: x-oogl.xml
Source11: x-oogl.desktop
#icons
Source20: hi16-app-geomview.png
Source21: hi22-app-geomview.png
Source22: hi32-app-geomview.png
Source23: hi48-app-geomview.png
Source24: hi64-app-geomview.png
Source25: hi128-app-geomview.png
Source26: hisc-app-geomview.svgz

BuildRequires: desktop-file-utils
BuildRequires: byacc flex
BuildRequires: gawk
# Until we have a generic BR: motif-devel -- Rex
BuildRequires: lesstif-devel
BuildRequires: libGL-devel libGLU-devel
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
BuildRequires: libXmu-devel
%else
# workaround http://bugzilla.redhat.com/211898
BuildRequires: xorg-x11-devel xorg-x11-Mesa-libGL xorg-x11-Mesa-libGLU
%endif
BuildRequires: tcl-devel tk-devel

#BuildRequires: /usr/bin/makeinfo 
BuildRequires: texinfo

#BuildRequires: /usr/bin/texi2html
%if 0%{?fedora} > 3 || 0%{?rhel} > 4
BuildRequires: texi2html
%else
BuildRequires: tetex
%endif

# for %_datadir/mimelnk
Requires: kde-filesystem
Requires: xdg-utils
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%if 0%{?libs}
Requires: %{name}-libs = %{version}-%{release}
%else
Obsoletes: %{name}-libs < %{version}-%{release}
Provides:  %{name}-libs = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%endif

%description
Geomview is an interactive 3D viewing program for Unix. It lets you view and
manipulate 3D objects: you use the mouse to rotate, translate, zoom in and out,
etc. It can be used as a standalone viewer for static objects or as a display
engine for other programs which produce dynamically changing geometry. It can
display objects described in a variety of file formats. It comes with a wide
selection of example objects, and you can create your own objects too.

%if 0%{?libs}
%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries
# include to paranoid, installing libs-only is still mostly untested
Requires: %{name} = %{version}-%{release}
# hack to help multilib upgrades (temporary)
Obsoletes: %{name} < %{version}-%{release}
# split happened here
#Obsoletes: geomview < 1.9.4-7 
%description libs
%{summary}.
%endif

%package devel
Summary: Development files for %{name} 
Group:   Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q 


%build
%configure \
  --enable-shared \
  --disable-static \
  --with-htmlbrowser=xdg-open \
  --with-pdfviewer=xdg-open \

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# .desktop entry
desktop-file-install --vendor="fedora" \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# mime
install -p -m644 -D %{SOURCE10} %{buildroot}%{_datadir}/mime/packages/x-oogl.xml

# mimelnk (kde3)
install -p -m644 -D %{SOURCE11} %{buildroot}%{_datadir}/mimelnk/object/x-oogl.desktop

# app icons
install -p -m644 -D %{SOURCE20} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/geomview.png
install -p -m644 -D %{SOURCE21} %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/geomview.png
install -p -m644 -D %{SOURCE22} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/geomview.png
install -p -m644 -D %{SOURCE23} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/geomview.png
install -p -m644 -D %{SOURCE24} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/geomview.png
install -p -m644 -D %{SOURCE25} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/geomview.png
install -p -m644 -D %{SOURCE26} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/geomview.svgz


# Unpackaged files
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/lib*.la


%clean
rm -rf %{buildroot}


%post
%{!?libs:/sbin/ldconfig}
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.gz ||:
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:
update-desktop-database -q > /dev/null 2>&1 ||:
update-mime-database %{_datadir}/mime > /dev/null 2>&1 ||:

%preun
if [ $1 -eq 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.gz ||:
fi

%postun
%{!?libs:/sbin/ldconfig}
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:
update-desktop-database -a > /dev/null 2>&1 ||:
update-mime-database %{_datadir}/mime > /dev/null 2>&1 ||:

%if 0%{?libs}
%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/*
%{_docdir}/geomview/
%{_datadir}/applications/*.desktop
%{_datadir}/geomview/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mimelnk/*
%{_datadir}/mime/packages/*.xml
%{_infodir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_libexecdir}/geomview/

%if 0%{?libs}
%files libs
%defattr(-,root,root,-)
%endif
%{_libdir}/libgeomview-%{version}.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgeomview.so
%{_includedir}/geomview/


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.9.4-8
- -libs: scriptlets

* Tue Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.9.4-7
- -libs subpkg, fixes multiarch conflicts (#341241) (f9+)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9.4-6
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.4-5
- fix x-oogl.desktop (to not include Patterns=*). doh.

* Tue Oct 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.4-4
- more icons (#190218)

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.4-3
- use model/vrml,object/x-oogl(register) mimetypes

* Mon Aug 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.4-2
- BR: gawk

* Mon Aug 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.4-1
- geomview-1.9.4

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-3
- License: LGPLv2+

* Mon Jul 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-2
- geomview.desktop: Categories=-Education (#241441)

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-1
- geomview-1.9.3

* Sat Jun 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.2-1
- geomview-1.9.2

* Wed Jun 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.1-1
- geomview-1.9.1
- omit orrery/maniview, can now be packaged separately.

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.25.rc9
- re-instate dfi --vendor=fedora (thanks Ville!) 

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.24.rc9
- fixup desktop-file-install usage
- fixup geomview.desktop Categories

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.22.rc9
- rename (man/man1/)sweep.1 -> geomview-sweep.1 to avoid
  Conflicts: lam (bug #212435)

* Sun Oct 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.21.rc9
- 1.8.2rc9

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.20.rc8
- fc6: BR: openmotif-devel -> lesstif-devel

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.19.rc8
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.18.rc8
- rename (man/man1/)animate.1 -> geomview-animate.1 to avoid 
  Conflicts: ImageMagick (bug #202039)

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.17.rc8
- 1.8.2-rc8
- -devel pkg

* Mon Jul 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.14.rc7
- BR: tcl-devel tk-devel

* Mon Jul 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.13.rc7
- 1.8.2-rc7

* Thu Jul 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.12.rc6
- 1.8.2-rc6

* Tue Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.11.rc4
- 1.8.2-rc4

* Fri Jul 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.10.rc3
- patch to fix ppc build

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.8.rc3
- 1.8.2-rc3
- --without-maniview (for now, doesn't build)
- drop -maniview, -orrery subpkgs

* Sat Jun 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.7.cvs20060623
- omit zero-length files

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.6.cvs20060623
- geomview-cvs20060623, (hopefully) will yield a usable, x86_64 build (#182625)
- --disable-seekpipe

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.5.cvs20040221
- BR: automake libtool

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.3.cvs20040221
- updated (transparent) icon (rh bug #190218)
- drop deprecated BR: libGL.so.1,libGLU.so.1 bits
- ExcludeArch: x86_64 (#182625)
- .desktop: MimeType: application/x-geomview

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Jan 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.2.cvs20040221
- rework Obsoletes/Provides: geomview-plugins

* Mon Jan 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.1.cvs20040221
- cvs20040421
- --with-xforms unconditional, Obsoletes/Provides: geomview-plugins

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]usres.sf.net> 1.8.1-12
- follow/use icon spec

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Sep 20 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-10
- update Source URL
- fix un-owned /usr/share/geomview/modules
- Requires(post,preun): /sbin-install-info
- -orrery: Requires: tk
- License: LGPL, %%doc COPYING
- comment out the Obsoleting of subpkgs with using --without.  I think
  the logic there is wrong.
- relax subpkgs to Requires: %{name} = %%epoch:%%version

* Tue Sep 14 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.9
- fix build for fc3
- remove unused gcc_ver cruft
- remove unused (by default) lesstif bits

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.8
- .desktop Categories += Education;Math;

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.7
- BR: libGL.so.1 libGLU.so.1

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.6
- fix file list (possible dups)

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.5
- BR: libtool flex
- BR: XFree86-devel (for lib{GL/GLU})

* Thu Jun 03 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.4
- .desktop: Categories += Graphics

* Tue Mar 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.3
- use patch from geomview sf site to allow gcc3.
- use desktop-file-install

* Wed Sep 24 2003 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.2
- cleanup for formal submission to fedora.

* Fri Aug 08 2003 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.1
- Build against openmotif.

* Mon May 12 2003 Rex Dieter <rexdieter at users.sf.net> 0:1.8.1-0.fdr.0
- fedora'ize
- rh73: link xforms static (for now, so rh80+ users could use if they
  want/need plugins/maniview subpkgs).
- rh80+: use g++296, no xforms.
- Obsoletes: subpkgs not built.

* Fri Jun 21 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-8
- Obsoletes/Provides: pluginname=version-release for extra plugins
  (so to gracefully handle upgrade from Mark's orrery rpm)

* Fri Jun 21 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-7
- use macros for all subpkgs
- include orrery-0.9.3.
- remove %_smp_mflags (makefile is not smp safe)

* Thu Jun 20 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-6
- include maniview-2.0.0.
- include geomview info/man pages.

* Thu Feb 27 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-5
- rebuild to link xforms dynamic

* Wed Feb 20 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-4
- conditionally use xforms (no by default)
- make subpkg require %%name-%%version-%%release
- tweak to work with new lesstif

* Tue Dec 11 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-3
- really use the app-icon this time.
- use Prefix to at least pretend relocatability

* Wed Nov 7 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-2
- make -plugins subpkg for plugins that use xforms.

* Fri Oct 5 2001 Rex Dieter <rexdieter at users.sf.net > 1.8.1-1
- cleanup specfile
- make icon/desktop files
- include option to link xforms-static (untested)

* Fri Sep 28 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-0
- first try.
- TODO: make subpkgs manual(html), modules, modules-xforms

