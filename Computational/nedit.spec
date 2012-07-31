Summary: A GUI text editor for systems with X
Name: nedit
Version: 5.5
Release: 23%{?dist}.1
Source: http://nedit.org/ftp/v5_5/nedit-%{version}-src.tar.bz2
Source1: nedit.desktop
Source2: nedit-icon.png
Patch0: nedit-5.5-security.patch
Patch1: nedit-5.4-makefiles.patch
Patch2: nedit-5.5-utf8.patch
Patch3: nedit-5.5-motif223.patch
Patch4: nedit-5.5-varfix.patch
Patch5: nedit-5.5-nc-manfix.patch
Patch6: nedit-5.5-visfix.patch
Patch7: nedit-5.5-nocsh.patch
Patch8: nedit-5.5-scroll.patch
URL: http://nedit.org
License: GPLv2
Group: Applications/Editors
Requires: openmotif, xorg-x11-fonts-ISO8859-1-75dpi
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openmotif-devel, libXau-devel, libXpm-devel, libXmu-devel
BuildRequires: desktop-file-utils
Requires: gtk2

%description
NEdit is a GUI text editor for the X Window System. NEdit is
very easy to use, especially if you are familiar with the
Macintosh or Microsoft Windows style of interface.

%prep
%setup -q
%patch0 -p1 -b .security
%patch1 -p1 -b .makefiles
%patch2 -p1 -b .utf8
%patch3 -p1 -b .motif223
%patch4 -p1 -b .varfix
%patch5 -p1 -b .nc-manfix
%patch6 -p1 -b .visfix
%patch7 -p1 -b .nocsh
%patch8 -p1 -b .scroll
for file in README doc/nedit.doc; do
  iconv -f latin1 -t utf8 < $file > $file.utf8
  touch -r $file $file.utf8
  mv $file.utf8 $file
done

%build
make linux C_OPT_FLAGS="$RPM_OPT_FLAGS -I/usr/include/openmotif" LD_OPT_FLAGS="-L%{_libdir}/openmotif"

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
mv source/nc source/nedit-client
install -m 755 source/nedit source/nedit-client $RPM_BUILD_ROOT%{_bindir}
install -p -m 644 doc/nedit.man $RPM_BUILD_ROOT%{_mandir}/man1/nedit.1x
mv doc/nc.man doc/nedit-client.man
install -p -m 644 doc/nedit-client.man $RPM_BUILD_ROOT%{_mandir}/man1/nedit-client.1x

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/nedit.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category "Development;" \
        %{SOURCE1}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%files
%defattr(-,root,root)
%doc doc/nedit.doc README ReleaseNotes
%{_mandir}/*/*
%{_bindir}/*
%{_prefix}/share/applications/*
%{_datadir}/icons/hicolor/

%changelog
* Tue Jan 11 2011 Josko Plazonic <plazonc@math.princeton.edu>
- require gtk2 to fix issues during kickstart phase

* Thu Jul  8 2010 Jindrich Novy <jnovy@redhat.com> 5.5-23
- remove (TM) from package description (#542473)
- build for EPEL-6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Jindrich Novy <jnovy@redhat.com> 5.5-20
- BR: xorg-x11-fonts-ISO8859-1 to avoid incorrect font
  substitutions (#464945)

* Fri Sep 26 2008 Jindrich Novy <jnovy@redhat.com> 5.5-19
- rediff security patch to be applicable with zero fuzz

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 5.5-18
- manual rebuild because of gcc-4.3 (#434192)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.5-17
- Autorebuild for GCC 4.3

* Sun Jan  6 2008 Patrice Dumas <pertusus@free.fr> 5.5-16
- minor cleanups

* Tue Oct 30 2007 Jindrich Novy <jnovy@redhat.com> 5.5-15
- make mouse wheel scrolling compatible with lesstif (#354591)

* Mon Oct 29 2007 Jindrich Novy <jnovy@redhat.com> 5.5-14
- don't use /bin/csh but /bin/sh as default shell (#355441)

* Fri Oct 26 2007 Jindrich Novy <jnovy@redhat.com> 5.5-13
- spec cleanup

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 5.5-12
- update License
- rebuild for BuildID

* Mon Jan  8 2007 Jindrich Novy <jnovy@redhat.com> 5.5-11
- explicitly depend on lesstif to avoid nedit crashes
  (binary lesstif/openmotif incompatibilities) (#221535)
- fix buildroot

* Sat Sep  2 2006 Jindrich Novy <jnovy@redhat.com> 5.5-10.fc6
- remove dependency on openmotif and build against lesstif
- add missing libXmu-devel dependency

* Wed Aug 30 2006 Jindrich Novy <jnovy@redhat.com> 5.5-9
- don't use the autodetected, but default visual to avoid
  crashes (#199770)

* Wed May 24 2006 Jindrich Novy <jnovy@redhat.com> 5.5-8
- don't strip binaries so that we have usable debuginfo
  nedit package (#192607)

* Sun Mar  5 2006 Jindrich Novy <jnovy@redhat.com> 5.5-7
- rebuild

* Thu Dec 16 2005 Jindrich Novy <jnovy@redhat.com> 5.5-6
- fix openmotif dependencies
- build with modular X

* Mon Oct 10 2005 Jindrich Novy <jnovy@redhat.com> 5.5-5
- update nedit file locations to new xorg standards (#167208, #170937)
- rename nc to nedit-client to avoid conflict with netcat and
  modify its manpage to reflect this
- fix License to GPL

* Wed Jul 27 2005 Jindrich Novy <jnovy@redhat.com> 5.5-4
- initial Extras built

* Mon Jan 20 2005 Jindrich Novy <jnovy@redhat.com> 5.5-3
- prepare the spec and desktop file for Extras inclusion

* Wed Jan 12 2005 Jindrich Novy <jnovy@redhat.com> 5.5-2
- fix usage of uninitialized variable (#144790)

* Mon Dec 27 2004 Jindrich Novy <jnovy@redhat.com> 5.5-1
- new version 5.5

* Mon Sep 20 2004 Jindrich Novy <jnovy@redhat.com>
- added nedit icon to be present in menus #131601
- updated spec to put it to the right place
- icon made by Joor Loohuis (joor@users.sourceforge.net)
- the icon processed by Peter Vrabec (pvrabec@usu.cz)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 5.4-1
- new version 5.4

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec  5 2003 Tim Waugh <twaugh@redhat.com>
- Don't explicitly require openmotif, since rpm does library dependencies
  automatically.
- Binary package doesn't require desktop-file-install.

* Fri Dec  5 2003 Tim Waugh <twaugh@redhat.com> 5.3-6
- Add ugly hack to work around openmotif's lack of UTF-8 support (bug #75189).
- Back-port 5.4RC2 fix for uninitialized variable (bug #110898).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Tim Waugh <twaugh@redhat.com> 5.3-3
- Handle X11 libdir issue.

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 5.3-2
- Remove original desktop file when installing.
- Fix desktop file icon (bug #61677).

* Wed Jul 24 2002 Karsten Hopp <karsten@redhat.de>
- 5.3
- use desktop-file-utils (#69461)
- redo all patches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Mar 22 2002 Tim Powers <timp@redhat.com>
- rebuilt against openmotif-2.2.2

* Fri Mar  1 2002 Than Ngo <than@redhat.com> 1.2-1
- update to 1.2
- cleanup patch files

* Thu Jan 17 2002 Than Ngo <than@redhat.com> 5.1.1-13
- rebuild against openmotif

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Oct 25 2001 Bill Nottingham <notting@redhat.com>
- 0 != NULL. lather, rinse, repeat. (#54943)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix crash while printing (#45149)
  I still think removing the package would be the better fix, though.

* Sun Jun 10 2001 Than Ngo <than@redhat.com>
- requires lesstif-devel

* Tue May 22 2001 Tim Powers <timp@redhat.com>
- patched to use lesstif

* Fri Apr 27 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix security bug, use mkstemp()

* Fri Oct 13 2000 Preston Brown <pbrown@redhat.com>
- .desktop file added

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jun 17 2000 Than Ngo <than@redhat.de>
- rebuilt against openmotif-2.1.30
- use PRM macros

* Tue May 16 2000 Tim Powers <timp@redhat.com>
- updated to 5.1.1
- updated URL and source location

* Wed Aug 18 1999 Tim Powers <timp@redhat.com>
- excludearch alpha

* Mon Jul 19 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Thu Apr 15 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Wed Oct 14 1998 Michael Maher <mike@redhat.com>
- built package for 5.2

* Thu May 21 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 5.0.2

* Thu Nov 20 1997 Otto Hammersmith <otto@redhat.com>
- added wmconfig

* Mon Nov 17 1997 Otto Hammersmith <otto@redhat.com>
- added changelog
- fixed src url
- added URL tag
