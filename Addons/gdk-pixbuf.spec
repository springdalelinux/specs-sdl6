Name:		gdk-pixbuf
Version:	0.22.0
Release:	38%{?dist}
Epoch:		1
Summary:	An image loading library used with GNOME
License:	LGPLv2+
Group:		System Environment/Libraries
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source2:	local-hack-gmodule2.tar.gz

Patch2:		gdk-pixbuf-0.18.0-gmodulehack.patch
# Quote in configure.in appropriately for recent libtool
Patch3:		gdk-pixbuf-0.22.0-acquote.patch
# Patches backported from GTK+ HEAD
Patch5:		gdk-pixbuf-0.22.0-bmp-colormap.patch
Patch6:		gdk-pixbuf-0.22.0-ico-width.patch
Patch7:		gdk-pixbuf-underquoted.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=150601
Patch8:		gdk-pixbuf-0.22.0-bmploop.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=130711
Patch10:	gdk-pixbuf-0.22.0-loaders.patch
Patch11:	gtk+-2.2.2-noexecstack.patch
Patch12:	gdk-pixbuf-0.22.0-bmpcrash.patch
Patch13:	gdk-pixbuf-0.22.0-xpm-largecol.patch
Patch14:	gdk-pixbuf-0.22.0-xpm-ncol-overflow.patch
Patch15:	gdk-pixbuf-0.22.0-xpm-whc-overflow.patch
# Modular X moves rgb.txt
Patch16:	gdk-pixbuf-0.22.0-rgb.patch
# multilib fixes
Patch17:	gdk-pixbuf-0.22.0-multilib.patch

URL:		http://developer.gnome.org/arch/imaging/gdkpixbuf.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	audiofile
BuildRequires:	autoconf, libtool, automake14
BuildRequires:	gtk+-devel, libpng-devel >= 1.2.2, libXt-devel

Obsoletes:	gdk-pixbuf-gnome < 1:0.22.0-29

%description
The gdk-pixbuf package contains an image loading library used with the
GNOME GUI desktop environment. The GdkPixBuf library provides image
loading facilities, the rendering of a GdkPixBuf into various formats
(drawables or GdkRGB buffers), and a cache interface.

%package devel
Summary:	Files needed for developing apps to work with the GdkPixBuf library
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries, header files, and include files
needed for developing applications that will work with the GdkPixBuf
image loading library.


%prep

%setup -q

%patch2 -p1 -b .gmodulehack
%patch3 -p1 -b .acquote

(cd gdk-pixbuf && tar zxf %{SOURCE2})

%patch5 -p1 -b .bmp-colormap
%patch6 -p1 -b .ico-width
%patch7 -p1 -b .underquoted
%patch8 -p1 -b .bmploop
%patch10 -p1 -b .loaders
%patch11 -p1 -b .noexecstack
%patch12 -p1 -b .bmpcrash
%patch13 -p1 -b .xpm-ncol-overflow
%patch14 -p1 -b .xpm-whc-overflow
%patch15 -p1 -b .xpm-largecol
%patch16 -p1 -b .rgb
%patch17 -p1 -b .multilib

perl -p -i.bak -e 's/gmodule.h/gmodule-local.h/g; s/g_module/local_hack_g_module/g; s/GModule/LocalHackGModule/g; s/G_MODULE/LOCAL_HACK_G_MODULE/g' gdk-pixbuf/gdk-pixbuf-io.c gdk-pixbuf/gdk-pixbuf-io.h
perl -pi -e 's/-static//g' gdk-pixbuf/local-hack-gmodule/Makefile

%build
libtoolize --copy --force
aclocal-1.4
automake-1.4
autoconf

(cd gdk-pixbuf/local-hack-gmodule && make && cp gmodule-local.h ..)

CFLAGS="$RPM_OPT_FLAGS" ./configure	\
	--prefix=%{_prefix} --sysconfdir=%{_sysconfdir}	 --libdir=%{_libdir}\
	--localstatedir=%{_localstatedir} --disable-gtk-doc

make

%install
rm -rf %{buildroot}
make prefix=%{buildroot}/%{_prefix} \
	sysconfdir=%{buildroot}/%{_sysconfdir} libdir=%{buildroot}/%{_libdir}\
	localstatedir=%{buildroot}/%{_localstatedir} install

# nuke .la files and .a files
find %{buildroot} -type f -name "*.a" -exec rm -f {} ';'
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%doc AUTHORS COPYING COPYING.LIB ChangeLog NEWS README TODO doc/*.txt doc/html
%{_libdir}/libgdk_pixbuf*.so.*
%dir %{_libdir}/gdk-pixbuf
%dir %{_libdir}/gdk-pixbuf/loaders
%{_libdir}/gdk-pixbuf/loaders/lib*.so*

%files devel
%defattr (-, root, root)
%{_includedir}/*
%{_bindir}/gdk-pixbuf-config
%{_libdir}/*so
%{_libdir}/*Conf.sh
%{_libdir}/pkgconfig/gdk-pixbuf.pc
%{_datadir}/aclocal/*
%{_datadir}/gnome/html/*

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 1:0.22.0-36
- Rebuild for gcc43

* Tue Aug 21 2007 Kevin Fenzi <kevin@tummy.com> - 1:0.22.0-35
- Correct License tag. 

* Thu Jan 25 2007 Kevin Fenzi <kevin@tummy.com> - 1:0.22.0-34
- Check in multilib patch. 

* Thu Jan 25 2007 Kevin Fenzi <kevin@tummy.com> - 1:0.22.0-33
- Add multilib handling patch (thanks mclasen at redhat.com)
- Add .pc file.

* Tue Dec 12 2006 Kevin Fenzi <kevin@tummy.com> - 1:0.22.0-32
- Take over maintainership and rebuild for fc7/devel.

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1:0.22.0-31
- Rebuild for FC6

* Sat Jun 24 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1:0.22.0-30
- don't require packages that don't exist

* Thu Jun 22 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1:0.22.0-29
- removed gnome subpackage, gnome-libs has been removed from core and extras
- removed .a file %%file list
- obsolete the gnome subpackage

* Tue Jun 20 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1:0.22.0-26
- remove "." from gnome sub package summary
- kill of .a files
- removed unused patches

* Sun Jun 18 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1:0.22.0-25
- spec tidy and fedora'ized

* Mon Jun 12 2006 Matthias Clasen <mclasen@redhat.com> 1:0.22.0-24
- Package review cleanup

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 0.22.0-23
- Build without gnome support, since Gnome 1 is on the way out

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 0.22.0-22
- BuildRequires: libXt-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.22.0-21.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.22.0-21.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-21
- Fix path of rgb.txt

* Wed Nov 16 2005 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-20
- Prevent another integer overflow in the xpm loader (#171901, CVE-2005-2976)
- Prevent an infinite loop in the xpm loader (#171901, CVE-2005-2976)
- Prevent an integer overflow in the xpm loader (#171073, CVE-2005-3186)

* Thu Nov 10 2005 Nalin Dahyabhai <nalin@redhat.com> - 1:0.22.0-19
- Rebuild because gtk+-devel lost its .la files, and our .la files want them.

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-18
- Fix a double free in the bmp loader

* Mon Mar  7 2005 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-17
- Mark libraries as non-execstack

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-16
- Rebuild with gcc4

* Fri Sep 24 2004 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-15.1
- Rebuild for RHEL4 without gnome support.

* Fri Sep 24 2004 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-15.0
- Rebuild for FC3 with gnome support.

* Wed Sep 15 2004 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-14
- Fix a bug in the last change which broke the xpm loader
- build without gnome support

* Wed Sep 15 2004 Matthias Clasen <mclasen@redhat.com> - 1:0.22.0-12
- Rebuild for FC3

* Tue Sep 14 2004 Bill Nottingham <notting@redhat.com> - 1:0.22.0-11
- build without gnome support

* Fri Aug 20 2004 Owen Taylor <otaylor@redhat.com> - 1:0.22.0-10.1.3
- Bump and rebuild for FC3

* Fri Aug 20 2004 Owen Taylor <otaylor@redhat.com> - 1:0.22.0-10.1.2
- Bump and rebuild for FC2

* Fri Aug 20 2004 Owen Taylor <otaylor@redhat.com> - 1:0.22.0-10.1.1
- Bump and build for FC1

* Fri Aug 20 2004 Owen Taylor <otaylor@redhat.com> - 1:0.22.0-10.0.3
- Bump and rebuild for 3.0E

* Fri Aug 20 2004 Owen Taylor <otaylor@redhat.com> - 1:0.22.0-10.0.2E
- Fix problem with infinite loop on bad BMP data (#130455,
  test BMP from Chris Evans, fix from Manish Singh)

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:0.22.0-9
- Fixed underquoted m4 definition.

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com>
- Make build

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar  5 2004 Owen Taylor <otaylor@redhat.com> 1:0.22.0-6.0.3
- Include /usr/lib/*.la for AS2.1

* Fri Mar  5 2004 Owen Taylor <otaylor@redhat.com> 1:0.22.0-6.0.2E
- Add some additional defines to work with 2.1AS

* Thu Mar  4 2004 Owen Taylor <otaylor@redhat.com> 1:0.22.0-6.1.1
- Bump and rebuild

* Thu Mar  4 2004 Owen Taylor <otaylor@redhat.com> 1:0.22.0-6.1.0
- Redo package to build without libtool-1.5 patch

* Wed Mar  3 2004 Owen Taylor <otaylor@redhat.com> 1:0.22.0-6.0.0
- Add a couple of bug-fixes backported from GTK+-2.x

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug 28 2003 Owen Taylor <otaylor@redhat.com> 1:0.22.0-4.0
- Rebuild for RHEL

* Wed Jul  9 2003 Owen Taylor <otaylor@redhat.com> 1:0.22.0-3.0
- Remove specific version from libtool requires

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 1:0.22.0-2.0
- Bump for rebuild

* Thu Jun 12 2003 Owen Taylor <otaylor@redhat.com> 1:0.22.0-1
- Version 0.22.0

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:0.18.0-8.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan  3 2003 Owen Taylor <otaylor@redhat.com>
- BuildRequires libtool (#80947, Alan)

* Thu Nov  7 2002 Jeremy Katz <katzj@redhat.com> 
- rebuild to fix X11 libdir on multilib arches
- use %%libdir, etc

* Tue Aug 27 2002 Elliot Lee <sopwith@redhat.com>
- Patch3 for #65823

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- fix warnings about unpackaged files (originally I was also fixing 
  libpng stuff but realized there was nothing to fix)

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com>
- remove -static from local-hack-gmodule Makefile, so that
  the shared libraries aren't DT_TEXTREL

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- 0.18

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Jeremy Katz <katzj@redhat.com>
- remove .la files

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Alex Larsson <alexl@redhat.com>
- Use autoconf 2.13

* Thu Feb 28 2002 Havoc Pennington <hp@redhat.com>
- backport to Hampton

* Thu Feb  7 2002 Havoc Pennington <hp@redhat.com>
- remove CPPFLAGS=-I/usr/include/png-1.0

* Thu Feb  7 2002 Havoc Pennington <hp@redhat.com>
- remove libpng10 linkage, add hack to dlopen without RTLD_GLOBAL

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com>
- bump release
- png1.0 stuff

* Wed Jan 23 2002 Havoc Pennington <hp@redhat.com>
- fix some prefix/lib->libdir type of stuff
- rebuild for db1 issues

* Wed Dec 19 2001 Jeremy Katz <katzj@redhat.com>
- 0.14

* Mon Oct 29 2001 Havoc Pennington <hp@redhat.com>
- 0.13

* Sat Oct  6 2001 Havoc Pennington <hp@redhat.com>
- fix glitch in my header relocation patch

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- cvs snap with headers relocated

* Fri Aug  3 2001 Owen Taylor <otaylor@redhat.com>
- Add dependency on gnome-libs-devel for the -devel package (#45020)

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Own /usr/lib/gdk-pixbuf, /usr/lib/gdk-pixbuf/loaders (#27423)
- Add BuildPrereq on gnome-libs-devel (#49444)
- Add --disable-gtk-doc (#48988)

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add post/postun for gnome subpackage

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch to cope with newer "file" version

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- copy config.{guess,sub} instead of calling libtoolize

* Wed Jun  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remember to set ownership in gnome subpackage

* Wed Jun 06 2001 Havoc Pennington <hp@redhat.com>
- Split out the gnome part into a separate package
- 0.11 upgrade
- don't libtoolize

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- New Version.

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Rebuild for GTK+-1.2.9 include paths

* Thu Feb 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libtoolize to make porting to new archs easy

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Owen Taylor <otaylor@redhat.com>
- Specfile fixes

* Thu Jun 15 2000 Owen Taylor <otaylor@redhat.com>
- Version 0.8.0

* Sat May  6 2000 Matt Wilson <msw@redhat.com>
- Red Hat-ified helix gdk-pixbuf RPM



