%define majorversion 2
%define minorversion 8
%define microversion 6

%define olpc_build 0

Summary: The AbiWord word processor
Name: abiword
Version: %{majorversion}.%{minorversion}.%{microversion}
Release: 3%{?dist}
Epoch: 1
Group: Applications/Editors
License: GPLv2+
Source0: http://abisource.com/downloads/abiword/%{version}/source/abiword-%{version}.tar.gz
Source1: http://abisource.com/downloads/abiword/%{version}/source/abiword-docs-%{version}.tar.gz
Source11: abiword.mime
Source12: abiword.keys
Source13: abiword.xml
URL: http://www.abisource.com/
Requires: libabiword = %{epoch}:%{version}-%{release}

%description
AbiWord is a cross-platform Open Source word processor. It is full-featured,
while still remaining lean.

%package -n libabiword
Summary: Library for developing applications based on AbiWord's core
Group: System Environment/Libraries
Patch0: abiword-2.6.0-windowshelppaths.patch
Patch1: abiword-2.8.3-desktop.patch
Patch2: abiword-2.6.0-boolean.patch
Patch3: abiword-plugins-2.6.0-boolean.patch
%if %{olpc_build}
Patch100: abiword-2.6.4-defaultfont.patch
Patch101: abiword-2.6.4-draghandles.patch
Patch102: abiword-2.6.4-nohtmloptions.patch
%endif

BuildRequires: autoconf, libtool
BuildRequires: desktop-file-utils
BuildRequires: fribidi-devel, enchant-devel, wv-devel
BuildRequires: zlib-devel, popt-devel, libpng-devel
BuildRequires: gtk2-devel, libgsf-devel
BuildRequires: boost-devel, t1lib-devel
BuildRequires: dbus-glib-devel >= 0.70
%if !%{olpc_build}
Requires: link-grammar >= 4.2.2
BuildRequires: readline-devel
BuildRequires: bzip2-devel
BuildRequires: poppler-devel >= 0.4.0
BuildRequires: ots-devel >= 0.4.2
BuildRequires: libwpd-devel >= 0.8.0
BuildRequires: libwpg-devel
BuildRequires: librsvg2-devel
BuildRequires: libwmf-devel
BuildRequires: aiksaurus-devel, aiksaurus-gtk-devel
BuildRequires: link-grammar-devel >= 4.2.2
BuildRequires: gtkmathview-devel >= 0.7.5, flex, bison
BuildRequires: loudmouth-devel
BuildRequires: asio-devel
BuildRequires: libsoup-devel
%endif

%description -n libabiword
Library for developing applications based on AbiWord's core.

%package -n libabiword-devel
Summary: Files for developing with libabiword
Group: Development/Libraries
Requires: libabiword = %{epoch}:%{version}-%{release}

%description -n libabiword-devel
Includes and definitions for developing with libabiword.

%prep
# setup abiword
%setup -q

# patch abiword
%patch1 -p1 -b .desktop
%patch2 -p1 -b .boolean
%if %{olpc_build}
%patch100 -p1 -b .defaultfont
%patch101 -p1 -b .draghandles
%patch102 -p1 -b .nohtmloptions
%endif

# patch abiword plugins
#%patch3 -p1 -b .boolean

# setup abiword documentation
%setup -q -T -b 1 -n abiword-docs-%{version}
%patch0 -p1 -b .windowshelppaths

%build
# build libabiword and abiword
cd $RPM_BUILD_DIR/abiword-%{version}
%if %{olpc_build}
%configure --disable-static --enable-dynamic --disable-gnomevfs --disable-gucharmap --disable-printing --enable-plugins="loadbindings collab" --enable-collab-backend-sugar
%else
%configure --disable-static --enable-dynamic --enable-plugins --enable-clipart --enable-templates
%endif
%{__make} %{?_smp_mflags}

# build the documentation
cd $RPM_BUILD_DIR/abiword-docs-%{version}
ABI_DOC_PROG=$(pwd)/../%{name}-%{version}/src/abiword ./make-html.sh

%install

# install abiword
cd $RPM_BUILD_DIR/abiword-%{version}
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# install the documentation
cd $RPM_BUILD_DIR/abiword-docs-%{version}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help
cp -rp help/* $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help/
# some of the help dirs have bad perms (#109261)
find $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help/ -type d -exec chmod -c o+rx {} \;

# finish up
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/
cp $RPM_BUILD_DIR/abiword-%{version}/abiword_48.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/abiword_48.png

cd $RPM_BUILD_DIR/abiword-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora --add-category X-Fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Red-Hat-Extra --remove-category X-Red-Hat-Base \
  --add-category Applications --add-category Office \
  ./abiword.desktop
# remove the original one (which has X-Red-Hat-Base)  (#107023)
%{__rm} -f $RPM_BUILD_ROOT/%{_datadir}/applications/abiword.desktop

%{__install} -p -m 0644 -D %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/mime-info/abiword.mime
%{__install} -p -m 0644 -D %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/mime-info/abiword.keys
%{__install} -p -m 0644 -D %{SOURCE13} $RPM_BUILD_ROOT%{_datadir}/mime/packages/abiword.xml

# nuke .la files
%{__rm} -f $RPM_BUILD_ROOT/%{_libdir}/libabiword-%{majorversion}.%{minorversion}.la
%{__rm} -f $RPM_BUILD_ROOT/%{_libdir}/%{name}-%{majorversion}.%{minorversion}/plugins/*.la

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%postun
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_bindir}/abiword
%{_datadir}/applications/*
%{_datadir}/mime-info/abiword.mime
%{_datadir}/mime-info/abiword.keys
%{_datadir}/mime/packages/abiword.xml
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/*.png
# Abiword help
%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord
%{_mandir}/man1/abiword.1.gz

%files -n libabiword
%doc $RPM_BUILD_DIR/%{name}-%{version}/COPYING $RPM_BUILD_DIR/%{name}-%{version}/COPYRIGHT.TXT
%{_libdir}/libabiword-%{majorversion}.%{minorversion}.so
%{_libdir}/%{name}-%{majorversion}.%{minorversion}
%{_datadir}/%{name}-%{majorversion}.%{minorversion}
# Abiword help - included in GUI app
%exclude %{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord

%files -n libabiword-devel
%{_includedir}/%{name}-%{majorversion}.%{minorversion}
%{_libdir}/pkgconfig/%{name}-%{majorversion}.%{minorversion}.pc

%changelog
* Wed Sep 29 2010 jkeating - 1:2.8.6-3
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Peter Robinson <pbrobinson@gmail.com> - 1:2.8.6-2
- Move abiword gui help from the library to the app. Fixes 578596

* Sat Aug 14 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.6-1
- New upstream release

* Sat Jun 05 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.5-1
- New upstream release

* Fri Apr 16 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.4-1
- New upstream release

* Thu Apr 08 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.3-2
- Update .desktop patch

* Thu Apr 08 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.3-1
- New upstream release

* Tue Mar 02 2010 Marc Maurer <uwog@abisource.com> - 1:2.8.2-1
- New upstream release
- Package the man page

* Wed Dec 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> -1:2.8.1-4
- Rebuild again since the wv soname bump was accidental
- Remove superflous BuildRoot definitions and removals

* Mon Dec 21 2009 Peter Robinson <pbrobinson@gmail.com> - 1:2.8.1-3
- Rebuild against new libwv

* Sun Nov 01 2009 Marc Maurer <uwog@abisource.com> - 1:2.8.1-2
- Rebuild

* Sun Nov 01 2009 Marc Maurer <uwog@abisource.com> - 1:2.8.1-1
- New upstream release

* Tue Sep 01 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.10-2
- Unconditionally add the dbus-glib-devel BR since the AbiCollab
  Sugar backend is now always compiled in, even on non-OLPC
  platforms.

* Sat Aug 29 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.10-1
- New upstream release

* Mon Aug 24 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.9-2
- Make abiword depend on libabiword

* Sun Aug 23 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.9-1
- New upstream version

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:2.7.8-2
- drop Req: mathml-fonts (dep moved to gtkmathview)

* Sun Aug 02 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.8-1
- New upstream version

* Mon Jul 27 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.7-3
- Rerun autogen.sh after changing the makefiles

* Mon Jul 27 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.7-2
- Add a patch to work around a templates makefile bug

* Mon Jul 27 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.7-1
- New upstream release
- Add --enable-dynamic to configure so plugins link against libabiword.so

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 05 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.6-3
- Re-add updated .desktop patch

* Sun Jul 05 2009 Peter Robinson <pbrobinson@gmail.com> - 1:2.7.6-2
- Remove old patch

* Sun Jul 05 2009 Peter Robinson <pbrobinson@gmail.com> - 1:2.7.6-1
- New upstream release

* Fri Jun 26 2009 Peter Robinson <pbrobinson@gmail.com> - 1:2.7.5-3
- Drop old dependencies. Fixes bug 506023

* Sun Jun 21 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.5-2
- Package unpackaged icon

* Fri Jun 19 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.5-1
- New upstream release

* Fri Jun 19 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.4-2
- Add libsoup-devel BR
- Remove version from asio-devel BR
- Add libwpg-devel BR
- Register the .abicollab extension and mimetype

* Thu Jun 11 2009 Marc Maurer <uwog@abisource.com> - 1:2.7.4-1
- New upstream release

* Mon Mar 09 2009 Marc Maurer <uwog@abisource.com> - 1:2.6.8-2
- Make g++ 4.4 and rindex friends again

* Mon Mar 09 2009 Marc Maurer <uwog@abisource.com> - 1:2.6.8-1
- New upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.6.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Marc Maurer <uwog@abisource.com> - 1:2.6.6-1
- New upstream release

* Sun Nov 23 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.5-1
- New upstream release

* Thu Nov 20 2008 Peter Robinson <pbrobinson@gmail.com> - 1:2.6.4-9
- Remove unused script to drop perl dependency

* Fri Sep 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.6.4-8
- add t1lib-devel to BuildRequires, fixes FTBFS

* Mon Jul 21 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-7
- Fix libabiword-devel requires

* Mon Jul 21 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-6
- Drop explicit libabiword requires

* Mon Jul 21 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-5
- Fix typo in patch name

* Mon Jul 21 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-4
- Merge with the OLPC-3 branch

* Sun Jul 13 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-3
- We don't include ispell_dictionary_list.xml anymore, so no
  need to ghost it

* Sun Jul 13 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-2
- Update patches to apply without fuzz

* Sun Jul 13 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.4-1
- New upstream release

* Thu May 01 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.3-1
- New upstream release

* Sun Apr 06 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.2-1
- New upstream release

* Sun Apr 06 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.1-1
- New upstream release

* Sat Mar 29 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-6
- Don't forget to cvs add nextgen.sh

* Sat Mar 29 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-5
- Include nextgen.sh as abiword-plugins it's a proper autoconf project
- Fix 439396: abiword includes its own dictionary?
- Don't build libabiword, it's broken; re-enable it when we release
  abiword 2.8, which generates a proper library
- Drop aspell-devel BR

* Sat Mar 29 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-4
- Don't forget to reautogen after changing the plugin build system

* Sat Mar 29 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-3
- Fix 439395: apply patch to remove any runtime dependency on boost

* Fri Mar 28 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-2
- Add BigEndian32.american.hash that was missing from the disted
  abiword-extras tarball

* Tue Mar 25 2008 Marc Maurer <uwog@abisource.com> - 1:2.6.0-1
- New upstream release
- Split off an experimental devel package

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:2.4.6-8
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Michel Salim <michel.sylvan@gmail.com> - 1:2.4.6-7
- Update license field
- Remove build deps on g++ and libstdc++ (in minimum build environment)
- Remove .cvsignore files from installed doc; fix abw2html.pl permission
- Add support for goffice-0.6 when building on Fedora 9 and above
- Fix for F9 glibc lacking TRUE and FALSE

* Tue Sep 04 2007 Lubomir Kundrak <lkundrak@redhat.com> - 1:2.4.6-6.fc7
- Fix 248103

* Fri Apr 06 2007 Marc Maurer <uwog@abisource.com> - 1:2.4.6-5.fc7
- Rebuild

* Fri Apr 06 2007 Marc Maurer <uwog@abisource.com> - 1:2.4.6-4.fc7
- Fix 234765

* Tue Feb 20 2007 Marc Maurer <uwog@abisource.com> - 1:2.4.6-3.fc7
- Fix 181799

* Fri Feb 02 2007 Marc Maurer <uwog@abisource.com> - 1:2.4.6-2.fc7
- Rebuild

* Sun Nov 05 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.6-1.fc7
- Update to 2.4.6

* Thu Oct 12 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.5-4.fc6
- Fix bug 207294

* Mon Sep 11 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.5-3.fc6
- Rebuild for FC6

* Sat Jul 22 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.5-2.fc6
- Fix http://bugzilla.abisource.com/show_bug.cgi?id=10229

* Sun Jul 09 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.5-1.fc6
- Update to 2.4.5
- Fix bug 196690 - abiword fails to build in mock with minimal 
  build environment
- Drop the document build patch

* Tue Apr 13 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.4-2.fc6
- Fix documentation generation
- Fix charting support

* Tue Apr 11 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.4-1.fc6
- New upstream version
- Remove the macro patch and update the desktop patch

* Wed Mar 29 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-8.fc6
- Rebuild

* Wed Mar 08 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-7.fc5
- Disable the collaboration plugin; it is not working in 2.4.x

* Thu Feb 16 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-6.fc5
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-5.fc5
- bug 171926

* Sat Jan 21 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-4.fc5
- Disable the PDF plugin for now, as poppler doesn't ship the xpdf
  headers anymore

* Sat Jan 14 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-3.fc5
- Remove redundant requires - bug 177305

* Thu Jan 05 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-2.fc5
- Bump release, forgot to add desktop patch

* Mon Jan 02 2006 Marc Maurer <uwog@abisource.com> - 1:2.4.2-1.fc5
- Update to 2.4.2
- Add BuildRequires readline-devel for the AbiCommand plugin
- Add BuildRequires bzip2-devel and poppler-devel for plugins
- Update desktop patch
- Patch to fix plugin marcros

* Wed Nov 09 2005 Marc Maurer <uwog@abisource.com> - 1:2.4.1-4.fc5
- Fix bug 171928

* Sun Oct 23 2005 Marc Maurer <uwog@abisource.com> - 1:2.4.1-3.fc5
- Fix bug 161832: "Abiword is not loading certain modules"
- Add libgsf dependecy, which was needed all along
- Disable the collaboration plugin, it is not for general use at all

* Tue Oct 11 2005 Marc Maurer <uwog@abisource.com> - 1:2.4.1-2
- Use %%{?dist} in the release name

* Sun Oct 9 2005 Marc Maurer <uwog@abisource.com> - 1:2.4.1-1
- Update to 2.4.1

* Mon Oct 3 2005 Marc Maurer <uwog@abisource.com> - 1:2.4.0-1
- Require mathml-fonts
- Don't rerun autogen.sh, no need anymore
- Update gtkmathview dependency to 0.7.5
- Update to 2.4.0

* Mon Sep 26 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.99-2
- Fix gtkmathview BuildRequires

* Thu Sep 22 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.99-1
- Update to 2.3.99

* Sat Sep 10 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.6-1
- Update to 2.3.6
- Drop the pango patch

* Sat Sep 3 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.5-3
- Rebuild

* Sat Sep 3 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.5-2
- Enable the abimathview plugin

* Sun Aug 21 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.5-1
- Update to 2.3.5

* Fri Aug 19 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.4-4
- Update the pango patch to disable more pango code

* Fri Aug 19 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.4-3
- Fix the build after applying the pango disabling patch by 
  rerunning autogen.sh

* Fri Aug 19 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.4-2
- Disable the experimental pango renderer

* Thu Aug 17 2005 Marc Maurer <uwog@abisource.com> - 1:2.3.4-1
- Update to 2.3.4
- Add link-grammar dependency

* Thu Jul 28 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.9-1
- Update to 2.2.9
- Drop the mailmerge patch again

* Sun Jun 6 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.8-2
- Fix build with mailmerge patch

* Sun Jun 6 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.8-1
- Update to 2.2.8

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1:2.2.7-2
- rebuild on all arches

* Mon Apr 4 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.7-1
- Because we love brown paper bag releases

* Sun Apr 3 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.6-1
- Drop the gcc4, wvread, virtdestr and pt64 patches
- Update the desktop patch

* Fri Mar 15 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.5-3
- Fix 64bit build
- Add virtual destructors to classes with virtual functions

* Fri Mar 14 2005 Marc Maurer <uwog@abisource.com> - 1:2.2.5-2
- Remove the --disable-magick plugin switch
- disable GDA support until the plugin is ported to gnomedb 1.2.x
- Change the download location from SF to http://www.abisource.com/
- patch libole2
- fix read as a macro in new glibc

* Fri Mar  2 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.5-1
- bump to latest stable
- drop integrated dashboard patch again
- some gcc4 fixes

* Wed Feb 23 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.4-2
- rh#149447# dashboard spam revisited

* Tue Feb 22 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.4-1
- bump to latest stable version
- drop integrated nautilus depend patch
- drop integrated libwpd depend patch

* Fri Feb 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.3-4
- upgrade to libwpd-0.8 and incoroprate necessary changeover patches

* Mon Feb 7 2005 Matthias Clasen <mclasen@redhat.com> - 1:2.2.3-3
- rebuild

* Mon Feb 2 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.3-2
- remove unneccessary nautilus dependency

* Mon Jan 17 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.3-1
- bump to new version
- drop integrated silenceabidash patch

* Fri Jan 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.2-4
- RH#145085# annoying cluepacket message on stdout/stderr

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 1:2.2.2-3
- Rebuilt for new readline.

* Tue Jan 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.2.2-2
- RH#143368# use enchant as spellchecker

* Mon Dec 13 2004 Caolan McNamara <caolanm@redhat.com> - 1:2.2.2-1
- bump to new version

* Mon Dec 6 2004 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-1
- bump to new version
- geometry patch upstreamed
- security patch upstreamed
- removeoledecod patch upstreamed
- regenerate desktop patch

* Mon Nov 22 2004 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-2
- #abi7961# remove tempnam usages

* Mon Nov 22 2004 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-1
- bump to latest major stable version
- #rh140321# sanity check geometry

* Tue Nov  9 2004 Caolan McNamara <caolanm@redhat.com> - 1:2.0.14-1
- bump to latest stable version

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1:2.0.12-4
- rebuild for python 2.4

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 1:2.0.12-3
- Change to PreReq instead of Requires(post), up to 0.9

* Thu Sep 29 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.12-2
- Better Requires desktop-file-utils

* Wed Sep 29 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.12-1
- update to new abiword, + change norwegian wordprocessor translation

* Tue Sep 14 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.11-3
- #132389# Add more abiword supported mime types to abiword.desktop

* Mon Sep 6 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.11-2
- merge abiword.keys into abiword.desktop

* Fri Aug 27 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.11-1
- 2.0.11

* Tue Aug 10 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.10-2
- use libgnomedb

* Tue Aug 10 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.10-1
- 2.0.10
- use aiksaurus

* Tue Aug 2 2004 Matthias Clasen <mclasen@redhat.com> 1:2.0.9-4
- rebuilt

* Thu Jul 29 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.9-3
- #126012# some desktop translations

* Wed Jul 28 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.9-2
- #128004# fix irritating windows looking filenames for generated pngs

* Fri Jul 16 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.9-1
- 2.0.9, new version with security fix

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.6-1
- 2.0.7, new version + gcc34 fixes

* Wed Apr 28 2004 Caolan McNamara <caolanm@redhat.com> 1:2.0.6-1
- 2.0.6, 64bit changes made upstream

* Sat Mar 13 2004 Jeremy Katz <> 1:2.0.5-1
- 2.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Jeremy Katz <katzj@redhat.com> - 1:2.0.3-3
- rebuild for newer libots and libwpd
- fix verify as non-root (#109261)
- add wpd files to abiword.keys (#114907)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Jeremy Katz <katzj@redhat.com> - 1:2.0.3-1
- 2.0.3 (fixes build against gtk+ 2.3 and lets us rebuild to fix libcroco dep)

* Wed Dec 17 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.2-2
- rebuild for new libwpd

* Sun Nov 30 2003 Jeremy Katz <katzj@redhat.com> 
- and librsvg2-devel (#111222)

* Fri Nov 28 2003 Jeremy Katz <katzj@redhat.com> 
- buildrequire libgnomeui-devel (#111164)

* Tue Oct 28 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.1-1
- 2.0.1
- really remove duplicate desktop file

* Tue Oct 21 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-6
- make the docs with the just built abiword so that we don't have to 
  have abiword installed to build the docs (#107279)

* Tue Oct 21 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-5
- fix linkage to glib 1.2 in hancom plugin (#106033)

* Sun Oct 19 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Tue Oct 14 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-4
- remove duplicate desktop file (#107023)

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-3
- include the help
- show the clipart (#104577)

* Mon Sep 15 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-2
- rebuild with newer libwpd and libots to get those plugins

* Sun Sep 14 2003 Jeremy Katz <katzj@redhat.com> 1:2.0.0-1
- 2.0.0

* Thu Sep  4 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.6-1
- 1.99.6

* Mon Aug 25 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.5-1
- 1.99.5

* Tue Aug  5 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.3-1
- 1.99.3
- put icon in the right place (#101646)
- fix some 64bit casting issues
- disable ots plugin for now, doesn't seem to build with ots 0.4.0 :/
- disable -pedantic -ansi so that it will build

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.2-2
- ugly hack to deal with libtool silliness on x86_64

* Fri Jul 11 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.2-1
- 1.99.2
- add buildrequires to make sure the ots and wp plugins get built
- no longer needs libgal2, remove buildrequires

* Mon Jun 16 2003 Jeremy Katz <katzj@redhat.com> 1:1.99.1-1
- 1.99.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 26 2003 Jeremy Katz <katzj@redhat.com> 1:1.9.1-3
- rebuild for new libgal2

* Mon May 19 2003 Jeremy Katz <katzj@redhat.com> 1:1.9.1-2
- tweak plugins build

* Mon May 12 2003 Jeremy Katz <katzj@redhat.com> 1:1.9.1-0.2
- 1.9.1
- drop old patches, switch to using autoconf based build system instead 
  of diving makefiles
- build with gnome support
- build with plugins
- add patch to build on AMD64

* Mon Apr 28 2003 Tim Powers <timp@redhat.com> 1:1.0.5-2
- rebuild to fix broken libpspell dep

* Mon Mar 24 2003 Jeremy Katz <katzj@redhat.com> 1:1.0.5-1
- 1.0.5

* Mon Feb 10 2003 Jeremy Katz <katzj@redhat.com> 1:1.0.4-2
- fix for abiword starting off the screen (#82425)

* Thu Jan 23 2003 Jeremy Katz <katzj@redhat.com> 1:1.0.4-1
- 1.0.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 29 2002 Jeremy Katz <katzj@redhat.com> 1:1.0.3-2
- make it build on x86_64

* Sun Dec 29 2002 Jeremy Katz <katzj@redhat.com> 1:1.0.3-1
- 1.0.3 (#80560)
- set umask before running mkfontdir in %%post
- patch AbiWord script to convert utf8 locales into non-utf8 variants (#72633)

* Mon Dec 02 2002 Elliot Lee <sopwith@redhat.com> 1.0.2-7
- Fix doc lines
- Fix multilib

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 1.0.2-6
- rebuilt with gcc-3.2 (we hope)

* Sat Aug 10 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-5
- fix help index symlink (#71219)

* Thu Aug  1 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-4
- add abiword binary symlink for upstream compatibility (#70267)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 1.0.2-3
- rebuild using gcc-3.2-0.1

* Thu Jul 18 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-2
- use included desktop file (#64447)
- use desktop-file-install

* Wed Jun 26 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-1
- 1.0.2
- disable perl module build since we weren't including it anyway

* Wed May 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.1-1
- 1.0.1

* Sun Apr 14 2002 Jeremy Katz <katzj@redhat.com> 0.99.5-1
- zh_CN and zh_TW fonts.dir were flipped
- update to 0.99.5 as it fixes some major bugs
- define ABI_BUILD_VERSION so the about screen gives us a version

* Mon Apr  8 2002 Bennhard Rosenkraenzer <bero@redhat.com> 0.99.4-2
- 1st try at fixing up CJK (#61590)
- #if 0'ify font warning dialog (#62909, #64556)

* Tue Apr  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.99.4-1
- Update to 0.99.4, fixes #61153
- Fix #61344
- Nuke the warning about being unable to add anything to font path,
  that's not how xfs works.

* Thu Feb 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.99.2-1
- 0.99.2
- remove blank lines in fonts.dir

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.99.1-1
- 0.99.1

* Wed Jan 30 2002 Alex Larsson <alexl@redhat.com> 0.9.5-3
- Added patch to use libpng10
- Added patch to fix perl build problems.

* Fri Nov 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.9.5-1
- 0.9.5

* Tue Oct 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.9.4.1-1
- Update to 0.9.4.1 (RFE #54806)
- Add URL (RFE #54590)

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.14-7
- Fix uninstall (#49350)

* Sat Jul  7 2001 Tim Powers <timp@redhat.com>
- rebuilt so that dirs aren't sgid root

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.14-5
- Add build requirements (#45157)

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.14-4
- Remove CVS admin files from documentation (#44916)

* Mon Jun 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x patch from <oliver.paukstadt@millenux.com>

* Sat Jun 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390 patch from Helge Deller

* Tue May 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.14-1
- Update to 0.7.14

* Tue Feb 27 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Handle MIME type stuff (Bug #27530)
- Add BuildPrereqs for some of the less common stuff AbiWord uses
  (gal-devel, gnome-print-devel, libunicode-devel)

* Tue Feb 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.13

* Mon Jan 15 2001 Than Ngo <than@redhat.com>
- fixed broken code for building

* Fri Dec 29 2000 Matt Wilson <msw@redhat.com>
- 0.7.12
- copy fonts.dir to fonts.scale so mkfontdir doesn't blow it away

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get rid of 0777 dirs

* Fri Nov 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.11

* Sun Aug 20 2000 Preston Brown <pbrown@redhat.com>
- fix path to chkfontpath, it was wrong.

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Mon Aug  7 2000 Jakub Jelinek <jakub@redhat.com>
- Don't ship AbiWord_s if we have AbiWord_d
- Register AbiWord's fontpath with xfs

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new libpng. This fixes Bug #13707 - gotta love it when they
  change the ABI without increasing the soname!
- fix tooltip (Bug #14711)
- move binaries from /usr/share to /usr/lib

* Wed Jul 12 2000 Jakub Jelinek <jakub@redhat.com>
- Fix build on ia64.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new gcc.

* Sat Jun 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build on ia64

* Fri Jun 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.10
- update download location

* Fri Jun  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial build for main CD
- clean up specfile
- fix build with gcc 2.96 and glibc 2.2
- exclude ia64 for now

* Wed May  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.9

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.8
- move the desktop file to /etc/X11/applnk so it can be used in both
  GNOME and KDE
- fix up handling of RPM_OPT_FLAGS

* Thu Jan 20 2000 Tim Powers <timp@redhat.com>
- bzipped source to conserve space.

* Sun Jan  9 2000 Matt Wilson <msw@redhat.com>
- enable GNOME, remove perl hack to do RPM_OPT_FLAGS
- added libpng requirement.  0.7.7 requires 1.0.5 libpng ABI

* Tue Jan  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.7
- handle RPM_OPT_FLAGS

* Mon Nov 15 1999 Tim Powers <timp@redhat.com>
- first build for inclusion into Powertools.
- some things in this spec file are from the abisuite-0.7.5-1mdk package
