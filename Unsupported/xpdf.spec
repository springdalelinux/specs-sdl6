Summary: A PDF file viewer for the X Window System
Name: xpdf
Version: 3.02
Release: 16%{?dist}
License: GPLv2
Epoch: 1
Url: http://www.foolabs.com/xpdf/
Group: Applications/Publishing

# There are some troublesome files named vms_*. We pull them out of the 
# tarball since we're not even using them on Linux.
# Source0: ftp://ftp.foolabs.com/pub/xpdf/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}-novms.tar.gz
# We have to pull the CMap files out due to non-free license.
# Source3: ftp://ftp.foolabs.com/pub/xpdf/xpdf-chinese-simplified-2004-jul-27.tar.gz
Source3: xpdf-chinese-simplified-2004-jul-27-NOCMAP.tar.gz
# Source4: ftp://ftp.foolabs.com/pub/xpdf/xpdf-chinese-traditional-2004-jul-27.tar.gz
Source4: xpdf-chinese-traditional-2004-jul-27-NOCMAP.tar.gz
# Source5: ftp://ftp.foolabs.com/pub/xpdf/xpdf-japanese-2004-jul-27.tar.gz
Source5: xpdf-japanese-2004-jul-27-NOCMAP.tar.gz
# Source6: ftp://ftp.foolabs.com/pub/xpdf/xpdf-korean-2005-jul-07.tar.gz
Source6: xpdf-korean-2005-jul-07-NOCMAP.tar.gz
# cyrillic and thai don't have CMap files to worry about.
Source7: ftp://ftp.foolabs.com/pub/xpdf/xpdf-cyrillic-2003-jun-28.tar.gz
Source8: ftp://ftp.foolabs.com/pub/xpdf/xpdf-thai-2002-jan-16.tar.gz
Source10: xpdf.desktop
Source11: xpdf.png
Source12: ftp://ftp.foolabs.com/pub/xpdf/xpdf-arabic-2003-feb-16.tar.gz
Source13: ftp://ftp.foolabs.com/pub/xpdf/xpdf-greek-2003-jun-28.tar.gz
Source14: ftp://ftp.foolabs.com/pub/xpdf/xpdf-hebrew-2003-feb-16.tar.gz
Source15: ftp://ftp.foolabs.com/pub/xpdf/xpdf-latin2-2002-oct-22.tar.gz
Source16: ftp://ftp.foolabs.com/pub/xpdf/xpdf-turkish-2002-apr-10.tar.gz

Patch0: xpdf-3.01-redhat-new.patch
Patch3: xpdf-2.02-ext.patch
Patch6: xpdf-3.00-core.patch
Patch7: xpdf-3.00-xfont.patch
Patch9: xpdf-3.00-papersize.patch
Patch10: xpdf-3.00-gcc4.patch
Patch11: xpdf-3.02-crash.patch
Patch12: xpdf-3.00-64bit.patch
# Patch13: xpdf-3.01-resize.patch
# Patch14: xpdf-3.01-freetype-internals.patch
Patch15: xpdf-3.01-nocmap.patch
Patch16: xpdf-3.02-fontlist.patch
Patch17: xpdf-3.02-x86_64-fix.patch
Patch18: xpdf-3.02-mousebuttons.patch
Patch19: xpdf-3.02-additionalzoom.patch
Patch20: xpdf-3.02-mousebuttons_view.patch

# Security patches
Patch100: xpdf-3.02pl1.patch
Patch101: ftp://ftp.foolabs.com/pub/xpdf/xpdf-3.02pl2.patch
Patch102: ftp://ftp.foolabs.com/pub/xpdf/xpdf-3.02pl3.patch
Patch103: ftp://ftp.foolabs.com/pub/xpdf/xpdf-3.02pl4.patch
Patch104: ftp://ftp.foolabs.com/pub/xpdf/xpdf-3.02pl5.patch

# Debian patches
Patch200: 02_permissions.dpatch
Patch201: 10_add_accelerators.dpatch
# Fix crash with ctrl-W in full screen mode
Patch202: fix-437725.dpatch
# Proper stream encoding on 64bit platforms
Patch203: fix-444648.dpatch
# Fix segfault in image handling
Patch204: fix-462544.dpatch
# Fix crash with "g" in full screen mode
Patch205: fix-479467.dpatch

Requires: urw-fonts
Requires: xdg-utils
Requires: poppler-utils
Requires: xorg-x11-fonts-ISO8859-1-75dpi
Requires: xorg-x11-fonts-ISO8859-1-100dpi

BuildRequires: openmotif-devel
BuildRequires: freetype-devel >= 2.1.7
BuildRequires: desktop-file-utils
BuildRequires: t1lib-devel
BuildRequires: libpaper-devel

Provides:  %{name}-chinese-simplified = %{version}-%{release}
Obsoletes: %{name}-chinese-simplified
Provides:  %{name}-chinese-traditional = %{version}-%{release}
Obsoletes: %{name}-chinese-traditional
Provides:  %{name}-korean = %{version}-%{release}
Obsoletes: %{name}-korean
Provides:  %{name}-japanese = %{version}-%{release}
Obsoletes: %{name}-japanese

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Xpdf is an X Window System based viewer for Portable Document Format
(PDF) files. Xpdf is a small and efficient program which uses
standard X fonts.

%prep
%setup -q -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 12 -a 13 -a 14 -a 15 -a 16
%patch0 -p1
%patch3 -p1 -b .ext
%patch6 -p1 -b .core
%patch7 -p1 -b .fonts
%patch9 -p1 -b .papersize
%patch10 -p1 -b .gcc4
%patch11 -p1 -b .crash
%patch12 -p1 -b .alloc
# Upstreamed
#%%patch13 -p1 -b .resize
#%%patch14 -p1 -b .freetype-internals
%patch15 -p1
%patch16 -p1 -b .fontlist
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

# security patches
%patch100 -p1 -b .security
%patch101 -p1 -b .security2
%patch102 -p1 -b .security3
%patch103 -p1 -b .security4
%patch104 -p1 -b .security5

# debian patches
%patch200 -p1 -b .permissions
%patch201 -p1 -b .accelerators
%patch202 -p1 -b .fullscreen-crashfix
%patch203 -p1 -b .64bit-stream
%patch204 -p1 -b .segfaultfix
%patch205 -p1 -b .fullscreen-crashfix2

%build
find -name "*orig" | xargs rm -f

# This may seem pointless, but in the unlikely event that _sysconfdir != /etc ...
for file in doc/*.1 doc/*.5 xpdf-*/README; do
  sed -i -e 's:/etc/xpdfrc:%{_sysconfdir}/xpdfrc:g' $file
done
# Same action for _datadir.
for file in xpdf-*/README xpdf-*/add-to-xpdfrc; do
  sed -i -e 's:/usr/share/:%{_datadir}/:g' $file
  sed -i -e 's:/usr/local/share/:%{_datadir}/:g' $file
done

%configure \
   --enable-multithreaded \
   --enable-wordlist \
   --with-x \
   --with-gzip \
   --enable-opi \
   --with-appdef-dir=%{_datadir}/X11/app-defaults/ \
   --without-Xp-library \
   --with-t1-library \
   --with-freetype2-library=%{_libdir} \
   --with-freetype2-includes=%{_includedir}/freetype2

make %{?_smp_mflags}
make xpdf %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/xpdf/arabic \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-simplified \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-traditional \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/cyrillic \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/greek \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/hebrew \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/japanese \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/korean \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/latin2 \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/thai \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/turkish \
         $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --vendor "fedora"                  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --add-category X-Fedora                         \
        %{SOURCE10}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/xpdf.png

cp -pr xpdf-arabic/* $RPM_BUILD_ROOT%{_datadir}/xpdf/arabic/
cp -pr xpdf-chinese-simplified/* $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-simplified/
cp -pr xpdf-chinese-traditional/* $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-traditional/
cp -pr xpdf-cyrillic/* $RPM_BUILD_ROOT%{_datadir}/xpdf/cyrillic/
cp -pr xpdf-greek/* $RPM_BUILD_ROOT%{_datadir}/xpdf/greek/
cp -pr xpdf-hebrew/* $RPM_BUILD_ROOT%{_datadir}/xpdf/hebrew/
cp -pr xpdf-japanese/* $RPM_BUILD_ROOT%{_datadir}/xpdf/japanese/
cp -pr xpdf-korean/* $RPM_BUILD_ROOT%{_datadir}/xpdf/korean/
cp -pr xpdf-latin2/* $RPM_BUILD_ROOT%{_datadir}/xpdf/latin2/
cp -pr xpdf-thai/* $RPM_BUILD_ROOT%{_datadir}/xpdf/thai/
cp -pr xpdf-turkish/* $RPM_BUILD_ROOT%{_datadir}/xpdf/turkish/

# poppler provides all utilities now
# http://bugzilla.redhat.com/bugzillA/SHow_bug.cgi?id=177446
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=219032
rm $RPM_BUILD_ROOT%{_bindir}/pdffonts
rm $RPM_BUILD_ROOT%{_bindir}/pdfimages
rm $RPM_BUILD_ROOT%{_bindir}/pdfinfo
rm $RPM_BUILD_ROOT%{_bindir}/pdftops
rm $RPM_BUILD_ROOT%{_bindir}/pdftotext
rm $RPM_BUILD_ROOT%{_bindir}/pdftoppm

rm $RPM_BUILD_ROOT%{_mandir}/man1/pdffonts.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdfimages.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdfinfo.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftops.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftotext.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftoppm.1*

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xpdf/
for i in arabic chinese-simplified chinese-traditional cyrillic greek hebrew japanese korean latin2 thai turkish; do
     mv $RPM_BUILD_ROOT%{_datadir}/%{name}/$i/README README.$i
     mv $RPM_BUILD_ROOT%{_datadir}/%{name}/$i/add-to-xpdfrc $RPM_BUILD_ROOT%{_sysconfdir}/xpdf/add-to-xpdfrc.$i
done

# xpdfrc cleanup
sed -i -e 's:/usr/local/share/:%{_datadir}/:g' $RPM_BUILD_ROOT%{_sysconfdir}/xpdfrc

# CJK are already in the file
for i in arabic cyrillic greek hebrew latin2 thai turkish; do
    echo "# $i" >> $RPM_BUILD_ROOT%{_sysconfdir}/xpdfrc
    echo "include %{_sysconfdir}/xpdf/add-to-xpdfrc.$i" >> $RPM_BUILD_ROOT%{_sysconfdir}/xpdfrc
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null ||:

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null ||:

%files
%defattr(-,root,root)
%doc CHANGES README README.*
%{_bindir}/xpdf
%{_mandir}/man?/xpdf*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdfrc
%dir %{_sysconfdir}/xpdf
%lang(ar) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.arabic
%lang(zh_CN) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.chinese-simplified
%lang(zh_TW) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.chinese-traditional
%lang(el) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.greek
%lang(iw) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.hebrew
%lang(ja) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.japanese
%lang(ko) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.korean
%lang(th) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.thai
%lang(tr) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.turkish
# cyrillic and latin2 are not langs, many languages are cyrillic/latin2
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.cyrillic
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.latin2
%{_datadir}/icons/hicolor/48x48/apps/xpdf.png
%dir %{_datadir}/xpdf
%{_datadir}/applications/*
%lang(ar) %{_datadir}/xpdf/arabic
%lang(zh_CN) %{_datadir}/xpdf/chinese-simplified
%lang(zh_TW) %{_datadir}/xpdf/chinese-traditional
%lang(el) %{_datadir}/xpdf/greek
%lang(iw) %{_datadir}/xpdf/hebrew
%lang(ja) %{_datadir}/xpdf/japanese
%lang(ko) %{_datadir}/xpdf/korean
%lang(th) %{_datadir}/xpdf/thai
%lang(tr) %{_datadir}/xpdf/turkish
%{_datadir}/xpdf/cyrillic
%{_datadir}/xpdf/latin2

%changelog
* Wed Nov 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-16
- apply xpdf-3.02pl5 security patch to fix:
  CVE-2010-3702, CVS-2010-3704

* Thu Jul  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-15.1
- use openmotif on EL-6

* Fri Oct 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-15
- apply xpdf-3.02pl4 security patch to fix:
  CVE-2009-3603, CVE-2009-3604, CVE-2009-3605, CVE-2009-3606
  CVE-2009-3608, CVE-2009-3609

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-13
- apply xpdf-3.02pl3 security patch to fix:
  CVE-2009-0799, CVE-2009-0800, CVE-2009-1179, CVE-2009-1180
  CVE-2009-1181, CVE-2009-1182, CVE-2009-1183

* Wed Mar  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-12
- add Requires: xorg-x11-fonts-ISO8859-1-100dpi (bz 485404)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.02-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-10
- cleanup crash patch a bit (bz 483664)
- improve support for more mouse buttons (bz 483669)

* Wed Dec 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-9
- apply debian patches

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1:3.02-8
- Fix Patch0:/%%patch mismatch.

* Thu Jun 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-7
- add missing Requires: xorg-x11-fonts-ISO8859-1-75dpi

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.02-6
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-5
- use xdg-utils instead of htmlview (bz 313311)

* Fri Nov  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-4
- resolve 372461, 372471, 372481

* Tue Aug 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-3
- fix PDF printing on x86_64 (bz 253601)
- add mouse buttons 8 and 9 (bz 255401)
- add extra zoom types (bz 251855)
- rebuild for BuildID

* Mon Aug  6 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-2
- fix font list parsing to squelch noise (bz 250709)
- cleanup add-to-xpdfrc files, update xpdfrc to include them by default

* Wed Aug  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-1
- bump to 3.02
- patch in security fix
- add arabic, greek, hebrew, latin2, turkish lang support

* Mon Dec 18 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-28
- Requires: poppler-utils

* Thu Dec 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-27
- drop the xpdf-utils subpackage, poppler-utils ate it all

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-26
- get rid of goo/vms_* since they have questionable licensing

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-25
- patch thai/cyrillic files for proper pathing

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-24
- get rid of non-free CMap files
- actually use thai/cyrillic sources
- patch out the references to using CMap files

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-23
- new patch missed README files, fixed

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-22
- use latest localized files
- fix redhat patch to work with new localized files

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-21
- use sane cp flags
- remove hardcoded X-Red-Hat-Base from .desktop
- mark the extra config files with their lang
- get rid of unnecessary Requires post,postun

* Sun Sep 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-20
- use the proper icon

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-19
- get rid of unnecessary BR fileutils, findutils
- get rid of duplicate R poppler-utils on main package
- use _sysconfdir/xpdf hierarchy, own add-to-xpdfrc as config files
- README files for each lang should be doc files, rename with lang ext
- ensure that files reflect macro settings
- use _sysconfdir macro
- remove files without -rf
- no need for /etc/X11/applnk/Graphics
- update xpdf-3.01-redhat.patch accordingly

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-18
- use t1lib
- remove non-utf8 character from old changelog
- put png icon in hicolor/48x48/apps
- use appropriate desktop scriptlets
- set vendor="fedora"
- move R:poppler-utils to xpdf-utils
- remove period from xpdf-utils summary
- add provides for everything we obsolete
- get rid of autoconf, Xprint patch, just pass --without-Xp-library
- add libpaper as BR

* Fri Sep 22 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-17
- move to Fedora Extras, use desktop-file-install

* Wed Aug 09 2006 Than Ngo <than@redhat.com> 1:3.01-16
- fix #200608, install icon in the wrong dir

* Fri Jul 14 2006 Than Ngo <than@redhat.com> 1:3.01-15
- fix build problem with new freetype

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-14.1
- rebuild

* Wed Jun 28 2006 Than Ngo <than@redhat.com> 1:3.01-14
- fix #197090, BR: autoconf

* Fri May  5 2006 Adam Jackson <ajackson@redhat.com> 1:3.01-13
- Remove spurious libXp dependency

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-12.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Than Ngo <than@redhat.com> 3.01-12
- apply patch to fix buffer overflow issue in the xpdf codebase
  when handling splash images CVE-2006-0301 (#179423)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-11.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Than Ngo <than@redhat.com> 3.01-11
- add correct app-defaults directory #178545

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.de> 3.01-10
- remove requires line in utils subpackage

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.de> 3.01-9
- remove pdf command-line utilities and require poppler ones
  instead (bug 177446).

* Wed Jan 18 2006 Than Ngo <than@redhat.com> 3.01-8
- add new subpackage xpdf-utils

* Tue Jan 10 2006 Karsten Hopp <karsten@redhat.de> 3.01-7
- add patches to fix CVE-2005-3191 and CAN-2005-3193

* Mon Dec 12 2005 Than Ngo <than@redhat.com> 3.01-6 
- rebuilt against new openmotif-2.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 Than Ngo <than@redhat.com> 3.01-5
- add correct Simplified/Traditional Chinese fonts #170989

* Tue Nov 08 2005 Than Ngo <than@redhat.com> 3.01-4
- get rid of XFree86-devel

* Thu Oct 13 2005 Matthias Clasen <mclasen@redhat.com> 3.01-3
- don't use freetype internals

* Fri Oct 07 2005 Than Ngo <than@redhat.com> 3.01-2 
- apply upstream patch to fix resize/redraw bug #166569

* Thu Aug 18 2005 Than Ngo <than@redhat.com> 3.01-1
- update to 3.01

* Thu Aug 11 2005 Than Ngo <than@redhat.com> 3.00-24
- change Kochi fonts to Sazanami fonts #165678

* Tue Aug 09 2005 Than Ngo <than@redhat.com> 3.00-23
- apply patch to fix xpdf DoS, CAN-2005-2097 #163918

* Mon Jul 25 2005 Than Ngo <than@redhat.com> 3.00-22
- fix allocation size 64bit architectures

* Mon Jul 25 2005 Than Ngo <than@redhat.com> 3.00-21
- fix xpdf crash #163807 

* Mon Jun 13 2005 Than Ngo <than@redhat.com> 3.00-20
- urlCommand launches htmlview #160176
- fix gcc4 build problem

* Mon May 23 2005 Than Ngo <than@redhat.com> 3.00-19
- apply patch to fix texts in non-embedded cjk font disappear, (#158509)

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 1:3.00-18
- rebuilt

* Thu Feb 10 2005 Than Ngo <than@redhat.com> 1:3.00-17
- More fixing of CAN-2004-0888 patch (bug #135393)

* Wed Jan 26 2005 Than Ngo <than@redhat.com> 1:3.00-16
- Add patch to fix handling CID font encodings in freetype version >= 2.1.8 (bug #135066)

* Thu Jan 20 2005 Than Ngo <than@redhat.com> 1:3.00-15
- Applied patch to fix CAN-2005-0064 (bug #145050)

* Wed Dec 22 2004 Tim Waugh <twaugh@redhat.com> 1:3.00-14
- Applied patch to fix CAN-2004-1125 (bug #143500).

* Mon Nov 29 2004 Than Ngo <than@redhat.com> 1:3.00-13
- set match as default psPaperSize #141131

* Tue Oct 26 2004 Than Ngo <than@redhat.com> 1:3.00-12
- bump release

* Tue Oct 26 2004 Than Ngo <than@redhat.com> 1:3.00-11
- don't link against t1lib, use freetype2 for rendering

* Thu Oct 21 2004 Than Ngo <than@redhat.com> 1:3.00-10
- apply patch to fix CAN-2004-0888

* Thu Oct 21 2004 Than Ngo <than@redhat.com> 1:3.00-9
- fix xpdf crash #136633

* Tue Oct 12 2004 Than Ngo <than@redhat.com> 1:3.00-8
- fix default fonts setting

* Mon Oct 11 2004 Than Ngo <than@redhat.com> 3.00-7
- fix locale issue #133911

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 1:3.00-6
- Fix xpdf crash when selecting outline without page reference,
  thanks Ulrich Drepper, bz #134993

* Thu Jun 24 2004 Than Ngo <than@redhat.com> 1:3.00-5
- update t1lib upstream
- add cjk font patch, thanks to Yukihiro Nakai, bug #123540
- fix a bug in font rasterizer, bug #125559
- improve menue entry, bug #125850

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 20 2004 Than Ngo <than@redhat.com> 3.00-3
- better fix for building with freetype 2.1.7

* Tue Feb 17 2004 Than Ngo <than@redhat.com> 3.00-2 
- t1lib-5.0.1

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 3.00-1
- 3.00 release
- add patch file to built with new freetype-2.1.7

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 1:2.03-1
- 2.03
- remove xpdf-2.02pl1.patch, which is included in 2.03
- fix warning issue (bug #106313)
- fix huge memory leak, (bug #89552)

* Tue Jul 29 2003 Than Ngo <than@redhat.com> 1:2.02-9
- rebuild

* Tue Jul 29 2003 Than Ngo <than@redhat.com> 1:2.02-8
- add missing icon (bug #100780) 
- fix a bug xpdf resource

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 2.02-7
- fixes a security hole

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May  5 2003 Than Ngo <than@redhat.com> 2.02-4.1
- merge sub packages to main package (bug #87750)

* Fri May  2 2003 Than Ngo <than@redhat.com> 2.02-3.1
- don't install backup files

* Mon Mar 31 2003 Than Ngo <than@redhat.com> 2.02-2
- build with freetype in RHL, #79680
- unsafe temporary files, #79682
- add Xfree86-devel in buildprereq
- build with -O0 on ppc, gcc bug

* Tue Mar 25 2003 Than Ngo <than@redhat.com> 2.02-1
- 2.02
- adjust some patch files for 2.02

* Tue Feb 18 2003 Than Ngo <than@redhat.com> 2.01-8
- own /usr/share/xpdf,  #73983
- remove debug unused infos, #84197

* Tue Feb  4 2003 Than Ngo <than@redhat.com> 2.01-7
- fix #82634

* Mon Feb  3 2003 Than Ngo <than@redhat.com> 2.01-6
- fix #82633

* Mon Jan 27 2003 Than Ngo <than@redhat.com> 2.01-5
- added locale patch from ynakai@redhat.com, bug #82638

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 20 2003 Than Ngo <than@redhat.com> 2.01-3
- Security fixes.

* Sun Dec  8 2002 Than Ngo <than@redhat.com> 2.01-2
- urlCommand launches htmlview (bug #76694)

* Fri Dec  6 2002 Than Ngo <than@redhat.com> 2.01-1
- update to 2.01

* Wed Nov  6 2002 Than Ngo <than@redhat.com> 2.00-1
- update to 2.00
- adapt a patch file for 2.00
- build against openmotif

* Fri Sep 20 2002 Than Ngo <than@redhat.com> 1.01-9
- Build against new freetype

* Mon Aug 26 2002 Than Ngo <than@redhat.com> 1.01-8
- add descriptive name (bug #71673)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 1.01-6
- desktop file issue (bug #69554)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 1.01-5
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.01-4
- automated rebuild

* Sun Jun 2 2002 Than Ngo <than@redhat.com> 1.01-3
- fix a bug in open file dialog (bug #39844)
- 1.01 handles Type 3 fonts (bug #48843)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 1.01-1
- xpdf-1.01, freetype-2.0.9

* Sun Mar 17 2002 Than Ngo <than@redhat.com> 1.00-3
- rebuild

* Wed Feb 21 2002 Than Ngo <than@redhat.com> 1.00-2
- fix Bad 'urlCommand' (bug #59730)

* Tue Feb 05 2002 Than Ngo <than@redhat.com> 1.00-1
- update to 1.00 (bug #59239, #48904)
- remove some patch files, which are included in 1.00
- sub packages for chinese-simplified, chinese-traditional, japanese and korean

* Fri Jan 25 2002 Than Ngo <than@redhat.com> 0.93-4
- rebuild in rawhide

* Mon Nov 12 2001 Than Ngo <than@redhat.com> 0.93-2
- enable Chinese GB font support
- enable Chinese CNS font support
- enable use of FreeType 2

* Mon Oct 29 2001 Than Ngo <than@redhat.com> 0.93-1
- update to 0.93

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Wed Mar 28 2001 Than Ngo <than@redhat.com>
- add german translation into desktop file
- move desktop file to /etc/X11/applnk/Graphics (Bug #32720)

* Tue Jan 02 2001 Than Ngo <than@redhat.com>
- added a default URL handler script with a corresponding definition
  in Xpdf, thanks to Michal Jaegermann <michal@harddata.com> (Bug #23112)

* Mon Dec 04 2000 Than Ngo <than@redhat.com>
- updated to 0.92 (Bug #16646)
- remove some patches, which included in xpdf-0.92

* Mon Oct 16 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Wed Oct 11 2000 Than Ngo <than@redhat.com>
- fix update problem (Bug #17924)

* Thu Aug 17 2000 Than Ngo <than@redhat.com>
- update to 0.91 (Bug #9961 and many major bugs) 

* Sun Aug 06 2000 Than Ngo <than@redhat.de>
- added swedish translation (Bug 15312)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 16 2000 Than Ngo <than@redhat.de>
- enable Japanese font support

* Fri Jun 16 2000 Preston Brown <pbrown@redhat.com>
- FHS paths
- better .desktop entry file

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- fix xpdf crashes on some data streams (Bug# 10154) (thanks Derek)
- add %%defattr
- use rpm macros

* Tue May 23 2000 Ngo Than <than@redhat.de>
- fix problem with loading fonts

* Sun May 21 2000 Ngo Than <than@redhat.de>
- put man pages in /usr/share/man/*
- update t1lib-1.0.1

* Mon May 08 2000 Trond Eivind Glomsrod <teg@redhat.com>
- fixed URL

* Fri Feb 11 2000 Preston Brown <pbrown@redhat.com>
- build for inclusion in 6.2.

* Wed Feb 09 2000 Jakub Jelinek <jakub@redhat.com>
- include decryption patches

* Mon Feb 07 2000 Presto Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- upgrade to xpdf 0.90, include t1lib Type1 rasterizer
- fix zapfdingbats font mapping issue

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Preston Brown <pbrown@redhat.com>
- converted wmconfig to desktop entry

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Nov 30 1998 Preston Brown <pbrown@redhat.com>
- updated to 0.80

* Fri Nov 06 1998 Preston Brown <pbrown@redhat.com>
- patched to compile with new, stricter egcs

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.7a

* Thu Nov 20 1997 Otto Hammersmith <otto@redhat.com>
- added changelog
- added wmconfig
