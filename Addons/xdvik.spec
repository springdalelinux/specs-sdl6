%bcond_without japanese
%define desktop_file_utils_version 0.9

# Set _texmf_main - this is defined in the texlive-texmf package 
%{!?_texmf_main: %define _texmf_main %{_datadir}/texmf}

Summary:        An X viewer for DVI files
Name:           xdvik
Version:        22.84.14
Release:        8%{?dist}
Url:            http://xdvi.sourceforge.net/
# encodings.c is GPLv2+ and LGPL and MIT
# read-mapfile.c tfmload.c are from dvips
# remaining is MIT
License:        GPLv2+
Group:          Applications/Publishing
Obsoletes:      tetex-xdvi < 3.0-99
Provides:       tetex-xdvi = 3.0-99
Provides:       xdvi = %{version}-%{release}
Obsoletes:      xdvi = 22.84.12
Requires:       tex(tex) tex(dvips)
Requires:       xdg-utils ghostscript
Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  t1lib-devel >= 5.0.2
BuildRequires:  Xaw3d-devel
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  autoconf213
BuildRequires:  libtool
BuildRequires:	tex(tex)
BuildRequires:  kpathsea-devel
%if %{with japanese}
BuildRequires:  freetype-devel >= 2.1.10
%endif

Source0:        http://kent.dl.sourceforge.net/sourceforge/xdvi/%{name}-%{version}.tar.gz
# Source30 is http://xdvi.sourceforge.net/xdvi48x48.gif converted to png
Source30:       xdvi48x48.png
%if %{with japanese}
Source100:      xdvi-ptex.map
%endif

# Fix handling of the 0 key. See:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2067614&group_id=23164&atid=377580
# https://bugzilla.redhat.com/show_bug.cgi?id=470942
# Fixed upstream post 22.84.14 ?
Patch0:		xdvik-22.84.14-zerofix.patch

%if %{with japanese}
# Japanese patch for xdvi from http://sourceforge.jp/projects/xdvi/
Patch1000:      xdvik-22.84.14-j1.40.patch.gz

# Patch to allow building of both xdvik and pxdvik.
# Local to Fedora, not appropriate to push upstream.
Patch1001:      xdvik-22.84.14-pxdvi.patch

%endif

# These patches would conflict with Patch1000 and friends and so must be applied
# after the xdvik directory has been copied to pxdvik
# Currently no patches of this type

%description
Xdvik, the kpathsea version of xdvi, is a previewer for DVI files
produced e.g. by the TeX or troff typesetting systems.

If you are installing texlive and you use PlainTeX or you are using DVI files,
you will also need to install xdvi which allows you to view DVI files.
Consider installing texlive-dvips (for converting .dvi files to PostScript
format for printing on PostScript printers), and texlive-latex (a higher level
formatting package which provides an easier-to-use interface for TeX).

%prep
%setup -q

# Fix handling of zero key
%patch0 -p1 -b .zerofix

# Allow Xaw3d enabled build of xdvi
sed -i 's|/Xaw/|/Xaw3d/|' texk/xdvik/gui/*.[ch] texk/xdvik/*.[ch]

%if %{with japanese}
# set up Japanese xdvi in its own directory
cp -a texk/xdvik texk/xdvik-orig

# This is the Japanese xdvi patch
%patch1000 -p1
mv texk/xdvik texk/pxdvik
mv texk/xdvik-orig texk/xdvik

# Build both the normal and the Japanese xdvi at the same time
%patch1001 -p1 -b .pxdvi

# XXX Is this really necessary?
mv texk/pxdvik/xdvi-ptex.sample texk/pxdvik/xdvi-ptex.sample.orig
install -p -m 644 %{SOURCE100} texk/pxdvik/xdvi-ptex.sample

%endif

# Re-run autoconf against patched Makefile.ins
( cd texk/xdvik ; autoconf-2.13 -m $RPM_BUILD_DIR/%{name}-%{version}/texk/etc/autoconf )
%if %{with japanese}
( cd texk/pxdvik ; autoconf-2.13 -m $RPM_BUILD_DIR/%{name}-%{version}/texk/etc/autoconf )
%endif
( cd texk ; autoconf-2.13 -m $RPM_BUILD_DIR/%{name}-%{version}/texk/etc/autoconf )

%build
# Here we go to great pains to avoid the automatic dependency generation from pulling in the 
# bundled kpathsea stuff
%configure --with-system-t1lib --with-system-kpathsea --with-xdvi-x-toolkit=xaw3d 

mv texk/kpathsea texk/kpathsea-keep

# Enable maintainer mode (see README_maintainer in tarball)
cp -p texk/make/rdepend.mk texk/make/rdepend.mk.maint
sed -i -e 's/@MAINT@//' texk/make/rdepend.mk

%if %{with japanese}
# configure pxdvi with more options
pushd texk/pxdvik
sh `grep "# ./con" config.status |sed -e s/^#\ //` --program-prefix=p --with-default-dvips-path=pdvips
popd

make -C texk/pxdvik/ depend
%endif

make -C texk/xdvik/ depend

mv texk/kpathsea-keep texk/kpathsea

%configure --with-system-t1lib --with-system-kpathsea --with-xdvi-x-toolkit=xaw3d

%if %{with japanese}
# configure pxdvi with more options
pushd texk/pxdvik
sh `grep "# ./con" config.status |sed -e s/^#\ //` --program-prefix=p --with-default-dvips-path=pdvips
popd
%endif

rm -rf libs texk/contrib/ texk/kpathsea

# Here we don't use make %{?_smp_mflags} since occasionally it fails
make

# Doc files (the full list of changes is in the texk/xdvik/CHANGES file)
iconv -f ISO-8859-1 -t UTF8 texk/xdvik/CHANGES -o CHANGES
touch -r texk/xdvik/CHANGES CHANGES
cp -p texk/xdvik/README.t1* .

%install
rm -rf $RPM_BUILD_ROOT

%if %{with japanese}
install_dirs='INSTDIRS=texk/xdvik texk/pxdvik'
%else
install_dirs='INSTDIRS=texk/xdvik'
%endif

# make install DESTDIR=$RPM_BUILD_ROOT doesn't work here
%makeinstall \
        texmf=$RPM_BUILD_ROOT%{_texmf_main} \
        texmfmain=$RPM_BUILD_ROOT%{_texmf_main} \
        "$install_dirs" \
        INSTALL='install -p'

# desktop file
cat > xdvi.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=DVI Viewer
Type=Application
Comment=DVI viewer for TeX DVI files
Icon=xdvi
MiniIcon=mini-doc1.xpm
Exec=xdvi
MimeType=application/x-dvi;
NoDisplay=true
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/

install -p  -m644 %{SOURCE30} $RPM_BUILD_ROOT%{_datadir}/pixmaps/
install -p  -m644 %{SOURCE30} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/xdvi.png
desktop-file-install --vendor "fedora" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Graphics \
  xdvi.desktop

# Remove uneeded file
rm $RPM_BUILD_ROOT%{_texmf_main}/release-tetex-src.txt

%if %{with japanese}
mkdir -p pxdvik/READMEs
pushd texk/pxdvik
for i in CHANGES.xdvik-jp README.xdvik-jp READMEs/* ; do
  iconv -f EUC-JP -t UTF-8 ${i} \
        -o  ../../pxdvik/${i}
  touch -r ${i} ../../pxdvik/${i}
done
popd
install -p -m 644 texk/pxdvik/xdvi-ptex.sample.orig pxdvik/xdvi-ptex.sample
%endif

%post
%{_bindir}/texconfig-sys rehash 2> /dev/null || :
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
%{_bindir}/texconfig-sys rehash 2> /dev/null || :
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README README.t1mapper README.t1fonts CHANGES 
%{_bindir}/oxdvi
%{_bindir}/xdvi
%{_bindir}/xdvi-xaw3d
%{_texmf_main}/xdvi/
%{_mandir}/man1/oxdvi.1*
%{_mandir}/man1/xdvi.1*
%{_datadir}/pixmaps/xdvi48x48.png
%{_datadir}/icons/hicolor/48x48/apps/xdvi.png
%{_datadir}/applications/fedora-xdvi.desktop

%if %{with japanese}
%doc pxdvik/
%{_bindir}/opxdvi
%{_bindir}/pxdvi
%{_bindir}/pxdvi-xaw3d
%{_texmf_main}/pxdvi/
%{_texmf_main}/fonts/map/pxdvi/
%endif

%changelog
* Wed Jan 27 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-8
- Add BuildRequires for tex(tex) to fix build (BZ 539119)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 22.84.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-6
- Correct paths in xdvi-ptex.map to fix BZ 508429 (Yuki Watanabe)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 22.84.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-4
- Add patch to fix zero key handling (BZ 470942)
- Remove texlive-2007-xprint.patch which actually hasn't been applied during
  22.84.14 packaging

* Sun Oct 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-3
- Fix package build breakage

* Sun Oct 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-2
- Fix previous spec file changelog entry
- Fix Japanese font handling (BZ 465391) by reworking pxdvi patch

* Fri Jul 18 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.14-1
- Update to version 22.84.14
- Update Japanese patch to 22.84.14-j1.40
- Rework patch allowing both normal and Japanese versions to be built
- Remove no longer needed patches that have been merged upstream:
- Various spec file fixups

* Sat May 10  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-20
- Update Japanese patch to xdvik-22.84.13-j1.40.patch.gz
- Rework patch to allow simultaneous building of xdvik and pxdvik - now called
  xdvik-22.84.13-pxdvi.patch
- Rename vfontmap to xdvi-ptex.map
- Rework patch to build pxdvik against system installed libraries - now called
  xdvik-22.84.13-pxdvi-use-system-libs.patch 

* Sun Apr 28  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-19
- Add more commentary about upstream status of patches
- No longer apply the texlive-xdvi-maxchar.patch patch

* Sun Apr 28  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-18
- Remove extraneous -r from cp command
- Add commentary about upstream status of patches
- Re-enable _texmf_main macro
- Add patch to fix window ID detection - BZ 442445

* Sun Feb  3  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-17
- Fix spec file typo

* Sun Feb  3  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-16
- Change directory copying logic such that we can use the upstream Japanese
  patch without modification

* Sat Feb  2  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-15
- Fix definition of _texmf_main for now
- Fix previous changelog entry version number

* Sat Feb  2  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-14
- Rework xdvik-22.84.13-uint32_t-fix.patch so as to be consistent with the
  upstream japanese patch and to stop the build barfing
- Remove parallel make since occasionally this fails

* Sat Feb  2  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-13
- Rework pxdvik-22.84.13-use-system-libs.patch for new japanes patch

* Sat Feb  2  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-12
- Fix errors in changelog
- Small modifications to xdvik-22.84.13-j1.36.patch.gz so it will apply cleanly

* Sat Feb  2  2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-11
- Update to Japanese patch xdvik-22.84.13-j1.36.patch.gz

* Wed Jan  23 2008 Patrice Dumas <pertusus@free.fr> - 22.84.13-10
- add xdg-utils, ghostscript requires
- use virtual requires for dvips and tex

* Mon Jan  21 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-9
- Add patch to fix segfault on double full screen toggle BZ 429429 (Michal Jaegermann)

* Sat Jan  19 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-8
- Add patch to fix spelling errors in manpage, derived from patch by A. Costa
  (BZ 429396)

* Wed Jan  16 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-7
- Replace texlive-2007-xdvi-keepflag.patch with
  xdvik-22.84.13-keepflag-fixscroll.patch to fix - BZ 417461 (Michal Jaegermann)

* Tue Jan  15 2008 Jindrich Novy <jnovy@redhat.com> - 22.84.13-6
- apply temporary file creation fix for xdvizilla
- better obsolete xdvi

* Tue Jan  15 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-5
- Added Requires(postun) for desktop-file-utils

* Mon Jan  14 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-4
- Use bcond for Japanese conditional stuff (Patrice Dumas)
- Fix license (Patrice Dumas)
- Make desktop file scriplets conform to packaging guidelines (Patrice Dumas)
- Remove unneeded Requires (Patrice Dumas)
- Adjust Provides and Obsoletes of xdvi

* Sun Jan  13 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-3
- Added xdg-open patch (Patrice Dumas)
- Avoid dependency generation implicating the bundled kpathsea files (Patrice Dumas)
- Added Requires for Xaw3d

* Sun Jan  13 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-2
- Add patch to build against system kpathsea rather than the one in the tarball
- Same patch also removes all includes to the t1lib headers shipped in the tarball to 
  prevent conflicts with system t1lib-devel
- Spefile cleanups

* Sun Jan  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 22.84.13-1
- Initial package based on the texlive.spec by Jindrich Novy
- Updated to latest upstream xdvik and Japanese xdvik 
- Reviewed all patches relating to xdvi in texlive.spec and cherry picked
  those that are still needed
- Reworked the patch to allow building of xdvik and pxdvik
