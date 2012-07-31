Name: mpg321
Version: 0.2.10.6
Release: 3%{?dist}
Summary: Command line MPEG audio player (fixed-point calculations)
Group: Applications/Multimedia
License: GPLv2+
URL: http://mpg321.sourceforge.net/
Source0: http://ftp.debian.org/debian/pool/main/m/mpg321/%{name}_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libao-devel
BuildRequires: libmad-devel
BuildRequires: libid3tag-devel
BuildRequires: zlib-devel
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives
Provides: mp3-cmdline = %{version}-%{release}

# alternatives priority
%define apriority 50

%description
mpg321 is a clone of the popular mpg123 command-line mp3 player. It should
function as a drop-in replacement for mpg123 in many cases. While some of
the functionality of mpg123 is not yet implemented, mpg321 should function 
properly in most cases for most people, such as for frontends such as
gqmpeg.

mpg321 is based on the mad MPEG audio decoding library. It therefore is
highly accurate, and also uses only fixed-point calculation, making it
more efficient on machines without a floating-point unit. It is not as
fast as mpg123 on systems which have a floating point unit.

%prep
%setup -q

%build
%configure \
	--disable-mpg123-symlink \
	--with-default-audio=pulse
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} INSTALL="install -p" install

# prepare ghost alternatives
# touch does not set the correct file mode bits 
%{__ln_s} -f %{name} %{buildroot}%{_bindir}/mpg123
%{__ln_s} -f %{name} %{buildroot}%{_bindir}/mp3-cmdline
%{__ln_s} -f %{name}.1 %{buildroot}%{_mandir}/man1/mpg123.1

%clean
%{__rm} -rf %{buildroot}

%post
if [ "$1" -eq 2 ]; then
	#clean old alternatives
	%{_sbindir}/alternatives \
		--remove mp3-cmdline %{_bindir}/mpg321 >/dev/null 2>&1
fi
manext=$(ls %{_mandir}/man1/%{name}.1* | sed '2,$ d; s/^.*\././')
[ "$manext" == ".1" ] && manext=""
%{_sbindir}/alternatives \
	--install %{_bindir}/mpg123 %{name}_binlink %{_bindir}/%{name} %{apriority} \
	--slave %{_mandir}/man1/mpg123.1$manext %{name}_manlink %{_mandir}/man1/%{name}.1$manext \
	--slave %{_bindir}/mp3-cmdline %{name}_mp3cmdline %{_bindir}/%{name} \
	>/dev/null 2>&1 ||:

%postun
if [ "$1" -eq 0 ]; then
	%{_sbindir}/alternatives \
		--remove %{name}_binlink %{_bindir}/%{name} >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog COPYING HACKING NEWS README* THANKS TODO
%ghost %{_bindir}/mp3-cmdline
%{_bindir}/%{name}
%ghost %{_bindir}/mpg123
%doc %{_mandir}/man1/%{name}.1*
%ghost %{_mandir}/man1/mpg123.1*

%changelog
* Wed Sep 29 2010 Adrian Reber <adrian@lisas.de> - 0.2.10.6-3
- rebuilt for #1399 (not possible to install mpg321)

* Sat May 02 2009 Adrian Reber <adrian@lisas.de> - 0.2.10.6-2
- fix man page alternatives link creation

* Mon Apr 06 2009 Luboš Staněk <lubek@users.sourceforge.org>  - 0.2.10.6-1
- upgrade more than a year old package for several fixes
- remove obsoletes to enable the real mpg123 package
- rework alternatives to enable the real mpg123 package
- use pulse as the default ao output
- relevant Debian's changelog:
  - Add large file support. (Closes: #152392).
  - Avoid crashing on non mp3 files. (Closes: #458035).
  - Don't scan file before playback. (Closes: #500102).
  - Don't leave dangling symlink. (Closes: #227713).
  - Make AM_PATH_AO XIPH_PATH_AO in configure.ac.
  - Escape hyphens in manpage.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.10.4-3
- rebuild for new F11 features

* Sun Sep 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.10.4-2
- rebuild

* Sat Oct 13 2007 Adrian Reber <adrian@lisas.de> - 0.2.10.4-1
- updated to debian's 0.2.10.4
- updated License
- adapted %%description, to make it not sound like mpg123 is non-free
- rebuilt for rpmfusion

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.2.10.3-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.10.3-2
- Avoid broken Requires(foo,bar) syntax.
- Specfile cleanups.
- Improve summary.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Jan  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.10.3-0.lvn.1
- Update to 0.2.10.3 (from Debian), fixes CAN-2003-0969.
- Make alsa09 the default output device.
- Install mpg123 manpage symlink.

* Sun Apr 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.10.1-0.fdr.1
- Update to 0.2.10.1 (from Debian).
- Rebuild using reorganized libmad.
- Provide mp3-cmdline virtual package and alternative.
- Save .spec in UTF-8.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.10-0.fdr.1
- Update to current Fedora guidelines.

* Thu Feb 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.2.10-1.fedora.1
- First Fedora release, based on Matthias Saou's work.
- Added zlib-devel build requirement.

* Mon Sep 30 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.2.10.
- Spec file cleanup.

* Tue Apr  9 2002 Bill Nottingham <notting@redhat.com> 0.2.9-3
- add patch from author to fix id3 segfaults (#62714)
- fix audio device fallback to match upstream behavior

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 0.2.9-2
- fix possible format string exploit
- add simple audio device fallback

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 0.2.9-1
- update to 0.2.9

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- update to 0.2.3, libmad is now separate

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 0.1.5
- fix build with new libao

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- initial build
