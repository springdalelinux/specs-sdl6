Summary: 	Library for reading and writing Quicktime files
Name: 		libquicktime
Version:	1.2.3
Release:	3%{?dist}
License:	LGPLv2+
Group: 		System Environment/Libraries
URL: 		http://libquicktime.sourceforge.net/
Source0: 	http://downloads.sourceforge.net/libquicktime/%{name}-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libdv-devel
BuildRequires:	libpng-devel libjpeg-devel libGLU-devel
BuildRequires:	libvorbis-devel ffmpeg-devel
BuildRequires:	schroedinger-devel
BuildRequires:	lame-devel alsa-lib-devel libXt-devel libXaw-devel libXv-devel
BuildRequires:	libdv-devel >= 0.102-4 x264-devel faad2-devel
BuildRequires:	libavc1394-devel libraw1394-devel >= 0.9.0-12
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:  schroedinger-devel
BuildRequires:  gettext-devel
%{?_with_faac:BuildRequires: faac-devel}

%package utils
Summary:	Utilities for working with Quicktime files
Group:		Applications/Multimedia

%package devel
Summary:	Development files for libquicktime
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} zlib-devel pkgconfig

# --------------------------------------------------------------------

%description
Libquicktime is based on the quicktime4linux library with several
enhancements. All 3rd-party libraries were removed from the
sourcetree. Instead, the systemwide installed libraries are detected
by the configure script. All original codecs were moved into
dynamically loadable modules, and new codecs are in
development. Libquicktime is source-compatible with
quicktime4linux. Special API extensions allow access to the codec
registry and more convenient processing of Audio and Video
data. 

%description utils
Libquicktime is based on the quicktime4linux library with several
enhancements. This package contains utility programs and additional
tools, like a commandline player and a GTK configuration utility which
can configure the parameters of all installed codecs.

%description devel
Libquicktime is based on the quicktime4linux library with several
enhancements. This package contains development files for %{name}.

# --------------------------------------------------------------------

%prep
%setup -q


# --------------------------------------------------------------------

%build
%configure \
	--enable-gpl \
	--disable-rpath \
	--with-cpuflags="$RPM_OPT_FLAGS" \
	--disable-dependency-tracking \
	--without-doxygen \
	--disable-static \
	--with-libdv \
	--enable-libswscale

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

# --------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT%{_libdir} -type f -a -name \*.la -exec rm {} \;


%find_lang %{name}


# --------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# --------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_libdir}/%{name}*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lqt_*.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/libquicktime_config
%{_bindir}/lqt_transcode
%{_bindir}/lqtplay
%{_bindir}/lqtremux
%{_bindir}/qt2text
%{_bindir}/qtdechunk
%{_bindir}/qtdump
%{_bindir}/qtinfo
%{_bindir}/qtrechunk
%{_bindir}/qtstreamize
%{_bindir}/qtyuv4toyuv
%{_mandir}/man1/lqtplay.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lqt/
%{_libdir}/pkgconfig/libquicktime.pc
%{_libdir}/%{name}*.so

# --------------------------------------------------------------------

%changelog
* Sun Sep  4 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.3-3
- Rebuilt for ffmpeg-0.8

* Fri Jul 15 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.3-2
- Rebuilt for x264 ABI 115

* Mon Jul 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.3-1
- Update to 1.2.3

* Fri Mar 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-2
- Rebuilt for new x264/FFmpeg

* Fri Jan 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-1
- Update to 1.2.2
- Add %%{_bindir}/lqtremux

* Sat Jul 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-2
- Add libquicktime-1.1.5-gtk.patch from Dan Horák.

* Sat May 01 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Jan 25 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.4-2
- Rebuild

* Sat Jan 16 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Fri Oct 30 2009 kwizart <kwizart at gmail.com > - 1.1.3-3
- Add BR schroedinger-devel

* Tue Oct 27 2009 kwizart <kwizart at gmail.com > - 1.1.3-2
- backport patch from Alexis Ballier.

* Thu Oct 15 2009 kwizart <kwizart at gmail.com > - 1.1.3-1
- Update to 1.1.3
- Conditionalize faac

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 1.1.1-2
- Rebuild for faad x264

* Sun Dec 28 2008 kwizart <kwizart at gmail.com> - 1.1.1-1
- Update to 1.1.1
- Disable lqt-config (Fix RPM Fusion #265 )

* Thu Dec  4 2008 kwizart <kwizart at gmail.com> - 1.1.0-1
- Update to 1.1.0

* Mon Sep 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.0.3-4
- rebuild for new x264

* Fri Aug 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.0.3-3
- rebuild

* Thu Jul 17 2008 kwizart <kwizart at gmail.com> - 1.0.3-2
- Add BR libdv-devel and --with-dv

* Thu Jul 17 2008 kwizart <kwizart at gmail.com> - 1.0.3-1
- Update to 1.0.3

* Sat Jun 14 2008 kwizart <kwizart at gmail.com> - 1.0.2-3
- Enable libswscale

* Thu Feb 28 2008 kwizart <kwizart at gmail.com> - 1.0.2-2
- Rebuild for gcc43 and x264

* Sun Jan 13 2008 kwizart <kwizart at gmail.com> - 1.0.2-1
- Update to 1.0.2 (gcc43 compliant)

* Mon Oct 15 2007 kwizart <kwizart at gmail.com> - 1.0.1-1
- Update to 1.0.1
- Disable libswscale (disabled in ffmpeg).

* Wed Sep 26 2007 kwizart <kwizart at gmail.com> - 1.0.0-2
- Fix build for new tooltip with gtk 2.12
  A better patch may need: 
  http://library.gnome.org/devel/gtk/unstable/gtk-migrating-tooltips.html

* Thu Jul  5 2007 kwizart <kwizart at gmail.com> - 1.0.0-1
- Update to 1.0.0
- Add BR gettext, libtool
- re-Run autogen.sh to prevent rpath issues...
- add patch from freshrpms.

* Fri Jan  5 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.9.10-4
- Drop old ffmpeg (main) package dependency.
- Improve summary.

* Wed Nov 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.10-3
- Enable GPL plugins, x264 patch borrowed from freshrpms.
- Split utilities into -utils subpackage.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.9.10-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Dams <anvil[AT]livna.org> - 0.9.10-1
- Disabled some standard library paths in rpath with Ville help
- Explicitly disabling static objects building

* Wed Sep 20 2006 Dams <anvil[AT]livna.org> - 0.9.10-1
- Updated to 0.9.10

* Sat Apr  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.8-1
- 0.9.8.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Jan  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.7-0.lvn.9
- Rebuild against new ffmpeg.
- Drop no longer needed modular X build dep workarounds.

* Thu Dec 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.9.7-0.lvn.8
- Adapt to modular X11.
- Drop unneeded GTK1 build dependencies, BuildRequire fixed libdv-devel.
- Drop zero Epochs.

* Fri Aug 19 2005 Dams <anvil[AT]livna.org> - 0:0.9.7-0.lvn.7
- More clean-up for obsolete pre-FC2 support

* Tue Aug 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.7-0.lvn.6
- Quick hack to fix libavcodec detection with newer (>= 20050731) ffmpegs.
- Don't ship static libs.

* Mon Jul  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.7-0.lvn.5
- Clean up obsolete pre-FC2 support.

* Thu Jun 16 2005 Dams <anvil[AT]livna.org> - 0:0.9.7-0.lvn.4
- .... and gtk+-devel.

* Thu Jun 16 2005 Dams <anvil[AT]livna.org> - 0:0.9.7-0.lvn.3
- libdv-devel needs glib-devel (fedora core bug....)

* Mon Jun 13 2005 Dams <anvil[AT]livna.org> - 0:0.9.7-0.lvn.2
- Updated tarball

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.7-0.lvn.1
- 0.9.7, MMX builds with gcc4 again.

* Sat May 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.6-0.lvn.1
- 0.9.6, aclocal18 patch applied upstream.
- Patch to compile with gcc4 (MMX build is borked though, build --without mmx).
- Use "make install DESTDIR=..." to avoid nasty rpaths.

* Thu Sep  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.3-0.lvn.2
- Make dv support conditional (default on), add minimum required libdv version.
- Make firewire support conditional again (only if dv support is available).
- Disable dependency tracking to speed up the build.
- Fix aclocal >= 1.8 warnings from lqt.m4.
- BuildRequire %%{_libdir}/libGLU.so.1.

* Mon Aug 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.3-0.lvn.1
- Update to 0.9.3.
- Enable ffmpeg plugin.
- Make firewire support unconditional.
- Fix 64bit libdir.
- Fix -devel dependencies.
- Update list of archs with MMX.
- Clean up list of docs.

* Tue Apr  6 2004 Dams <anvil[AT]livna.org> 0:0.9.2-0.lvn.2
- BuildConflicts libraw1394 0.10.0 to prevent surprises.

* Tue Apr  6 2004 Dams <anvil[AT]livna.org> 0:0.9.2-0.lvn.1
- Conditionnal firewire stuff rewriten

* Wed Mar 10 2004 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.1
- Updated to final 0.9.2 release
- firewire now default enabled

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.7.pre1
- Removed comment after scriptlets

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.6.pre1
- Without firewire BuildConflicts with libdv/libavc1394/libraw1394-devel

* Mon Jul 14 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.5.pre1
- Added missing deps for ffmpeg-devel
- Added build option "with firewire" (disabled by default)

* Wed Jul  9 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.4.pre1
- Added missing unowned directory 
- Removed URL in Source0
- buildroot -> RPM_BUILD_ROOT
- athlon is mmx compliant too 
- Now include all *.so/*.so.*/.a in libdir (bug #451)

* Wed Apr 23 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.3.pre1
- Typo in group tag

* Mon Apr 21 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.0.2.pre1
- Major fix from from Diag (plugins are now in the package).

* Wed Apr 16 2003 Dams <anvil[AT]livna.org> 
- Initial build.	
