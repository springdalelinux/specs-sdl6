Name:           fluxbox
Version:        1.1.1
Release:        5%{?dist}

Summary:	Window Manager based on Blackbox

Group:          User Interface/Desktops
License:        MIT
URL:            http://fluxbox.sourceforge.net

Source0:        http://download.sourceforge.net/fluxbox/fluxbox-1.1.1.tar.bz2
Source3:        fluxbox.desktop
Source4:        fluxbox-xdg-menu.py
Patch0:         fluxbox-startfluxbox-pulseaudio.patch
Patch1:         fluxbox-gcc43.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  imlib2-devel
BuildRequires:	zlib-devel
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libtool
Requires:       pyxdg
Requires:       artwiz-aleczapka-fonts

%description

Fluxbox is yet another windowmanager for X.  It's based on the Blackbox 0.61.1
code. Fluxbox looks like blackbox and handles styles, colors, window placement
and similar thing exactly like blackbox (100% theme/style compatibility).  So
what's the difference between fluxbox and blackbox then?  The answer is: LOTS!

Have a look at the homepage for more info ;)

%package pulseaudio
Group:          User Interface/Desktops
Summary:        Enable pulseaudio support
Requires:       %{name} = %{version}-%{release}
Requires:       alsa-plugins-pulseaudio
Requires:       pulseaudio pulseaudio-module-x11 pulseaudio-utils
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
BuildArch:      noarch
%endif

%description pulseaudio
Enable pulseaudio support.

%prep
%setup -q
%patch0
%patch1 -p1 -b .gcc43

%build
%configure      --enable-xft \
                --enable-gnome \
                --enable-kde \
                --enable-xinerama \
		--enable-imlib2 \
		--enable-nls \
		--x-includes=%{_includedir} \
		--x-libraries=%{_libdir} \
		--disable-static

make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# this is for Fedora Core
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions/
install -m 0644 -p %SOURCE3 $RPM_BUILD_ROOT%{_datadir}/xsessions/
install -m 0755 -p %SOURCE4 $RPM_BUILD_ROOT%{_bindir}/fluxbox-xdg-menu

# fix 388971
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
touch -r ChangeLog $RPM_BUILD_ROOT/%{_sysconfdir}/fluxbox-pulseaudio

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/%{name}
%{_datadir}/xsessions/fluxbox.desktop

%files pulseaudio
%defattr(-,root,root,755)
%{_sysconfdir}/fluxbox-pulseaudio

%changelog
* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-5
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.1-3
- make -pulseaudio package noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 18 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.1-1
- version upgrade

* Sat Sep 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.0.1-1
- version upgrade

* Wed Sep 03 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.0-1
- version upgrade

* Thu Mar 27 2008 Christopher Aillon <caillon@redhat.com> - 1.0.0-5
- Fix the build against GCC 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-4
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.0.0-3
- Rebuilt for gcc43

* Thu Jan 03 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-2
- add subpage -pulseaudio to fix #388971: fluxbox fails to start pulseaudio
  at login

* Mon Oct 08 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-1
- version upgrade

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.0-0.3.rc3
- rebuild for buildid

* Sun Jun 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-0.2.rc3
- fix #242187

* Tue Mar 20 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-0.1.rc3
- version upgrade
- fix #236509
- fix #229307

* Sat Oct 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15.1-3
- fix #209347,#196106, and #187740

* Wed Sep 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15.1-2
- FE6 rebuild

* Wed Apr 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15.1-1
- version upgrade

* Mon Apr 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15-2
- fix #187734

* Sun Mar 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15-1
- version upgrade

* Thu Mar 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-3
- fix Requires
- patch startfluxbox to generate user menu
- fix gdm detection

* Thu Mar 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-2
- fix build on gcc41

* Thu Nov 10 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- enable nls and imlib2
- require artwizaleczepka instead of providing it...
- add menu script from Rudolf Kastl

* Thu Sep 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-1
- version upgrade

* Tue Sep 06 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-4
- remove X11R6 path stuff #167601

* Thu Jun 16 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-3.fc4
- fix #160614

* Wed Jun 08 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-2.fc4
- fix generate menu bug and revisit switches

* Tue May 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- upgrade to 0.9.13

* Wed Apr 13 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.9-4
- Fix build for GCC 4.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Nov 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.9-2
- Fix build for GCC 3.4.

* Mon Apr 26 2004 Arnaud Abélard
- rebuilt against Fluxbox-0.9.9

* Thu Jan 16 2004 Arnaud Abélard
- now using artwiz-aleczapka as the artwiz-fonts

* Thu Jan 16 2004 Arnaud Abélard
- fixed a bug with the artwiz fonts

* Thu Jan 15 2004 Arnaud Abélard
- rebuilt against Fluxbox-0.9.8

* Sun Jan 11 2004 Arnaud Abélard
- Added Artwiz nice fonts

* Sat Jan 10 2004 Arnaud Abélard
- rebuild against Fluxbox-0.9.7

* Sat Jan 11 2003 Che
- rebuild without debug

* Mon Dec 09 2002 Che
- new version 0.1.14

* Tue Nov 19 2002 Che
- new version 0.1.13

* Tue Oct 30 2002 Che
- fixed gdm entry

* Tue Oct 23 2002 Che
- added a gdm entry :)

* Tue Oct 22 2002 Che
- initial rpm release

