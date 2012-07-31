%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
Summary: Adobe Flash Player 10.3
Name: flash-plugin
Version: 10.3.181.14
Release: 2
License: Commercial
Group: Applications/Internet
Packager: Adobe Systems Inc.
Vendor: Adobe Systems Inc.
URL: http://www.adobe.com/downloads/
Source: flash-plugin-10.3.181.14-release.i386.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: glibc >= 2.4, /bin/sh
Provides: kcm_adobe_flash_player.so, libflashplayer.so, flash-plugin = 10.3.181.14-release

%description
Adobe Flash Plugin 10.3.181.14
Fully Supported: Mozilla SeaMonkey 1.0+, Firefox 1.5+, Mozilla 1.7.13+

Originally done with rpm version 4.3.3,
built on fplayerbuild6-lnx.macromedia.com at Tue May 10 13:17:21 2011
from flash-plugin-10.3.181.14-release.src.rpm with opt flags -O2 -g -pipe -m32 -march=i386 -mtune=pentium4

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ "$1" = "1" ]; then
    /usr/lib/flash-plugin/setup install
fi
if [ "$1" = "2" ]; then
    /usr/lib/flash-plugin/setup upgrade
fi

ln -f -s /usr/share/icons/hicolor/48x48/apps/flash-player-properties.png /usr/share/pixmaps/


%preun
if [ "$1" = "0" ]; then
    /usr/lib/flash-plugin/setup preun
fi


%postun
rm -f /usr/share/pixmaps/flash-player-properties.png

%files
%dir %attr(0755,root,root) /usr/lib/flash-plugin
%attr(0644,root,root) /usr/lib/flash-plugin/LICENSE
%attr(0644,root,root) /usr/lib/flash-plugin/README
%attr(0744,root,root) /usr/lib/flash-plugin/homecleanup
%attr(0755,root,root) /usr/lib/flash-plugin/libflashplayer.so
%attr(0755,root,root) /usr/lib/kde4/kcm_adobe_flash_player.so
%attr(0755,root,root) %{_bindir}/flash-player-properties
%attr(0744,root,root) /usr/lib/flash-plugin/setup
%dir %attr(0755,root,root) /usr/share/doc/flash-plugin-%{version}
%doc %attr(0644,root,root) /usr/share/doc/flash-plugin-%{version}/readme.txt
%attr(0644,root,root) %{_datadir}/applications/flash-player-properties.desktop
%attr(0644,root,root) %{_datadir}/kde4/services/kcm_adobe_flash_player.desktop
%attr(0755,root,root) %{_datadir}/icons/hicolor/*/apps/flash-player-properties.png



%triggerin -- firefox
/usr/lib/flash-plugin/setup upgrade

%changelog
* Fri May 13 2011 Thomas Uphill <uphill@ias.edu> 10.3-2
- update to 10.3
- add flash properties bin and desktop
- fix bad permissions on hicolor dir


* Tue Dec 12 2006 Warren Togami <wtogami@redhat.com> 9.0.21.55-4
- more spec and script cleanups
- update LICENSE

* Sat Nov 11 2006 Warren Togami <wtogami@redhat.com> 9.0.21.55-3
- Flash Player 9 beta
- Massive cleanup:
    no longer requires click-thru EULA
    no longer requires XPCOM integration
    other script and spec simplifications

* Tue Sep 12 2006 Warren Togami <wtogami@redhat.com> 7.0.68-1
- CVE-2006-3311 CVE-2006-3587 CVE-2006-3588

* Wed Mar 15 2006 Warren Togami <wtogami@redhat.com> 7.0.63-1
- CVE-2006-0024

* Tue Nov 08 2005 Warren Togami <wtogami@redhat.com> 7.0.61-1
- #172731 7.0.61 CVE-2005-2628
- #163713 Fix setup script so it no longer errors on Firefox 1.5+

* Sat Nov 06 2004 Warren Togami <wtogami@redhat.com> 7.0.25-2
- add triggers for mozilla, firefox, opera
- RPM scriptlets: only output messages for errors

* Fri May 28 2004 Warren Togami <warrren@togami.com> 7.0.25-1
- update to 7.0.25
- scan for versioned firefox dirs

* Sun Mar 14 2004 Warren Togami <warren@togami.com> 6.0.81-1
- update to 6.0.81 (Security)
- no longer requires libstdc++
  Should solve XPCOM integration javascript problems with gcc-3.x compiled Mozilla
- i386 binary only
- really fix dir ownership
- support firefox
- gtk2 click-thru

* Fri Nov 21 2003 Warren Togami <warren@togami.com> 6.0.79-2
- Cleanup ugly hacks in spec and modernize to most fedora.us standards.
- Drop Phoenix support, add MozillaFirebird and mozilla-firebird
- Generate xpti.dat for all browsers in a generic way
  This should fix javascript integration.

* Thu Mar 06 2003 Warren Togami <warren@togami.com> 6.0.79-1
- Important security update
- http://www.macromedia.com/devnet/security/security_zone/mpsb03-03.html

* Thu Dec 12 2002 Warren Togami <warren@togami.com> 6.0.69-6
- sync with final tarball (same binary though)

* Wed Dec 11 2002 Warren Togami <warren@togami.com> 6.0.69-5
- add setup complete message

* Sat Dec 07 2002 Warren Togami <warren@togami.com> 6.0.69-4
- fix minor suse uninstall glitch

* Fri Dec 06 2002 Warren Togami <warren@togami.com> 6.0.69-3
- patch to show-license.c, thanks to Bill Tompkins
- textmode EULA interface

* Fri Dec 06 2002 Warren Togami <warren@togami.com> 6.0.69-2
- beta of "Lawyer Appeasement Edition"
- show-license.c, thanks to Daniel Elstner
- scripts separated from .spec into "setup"

* Wed Dec 04 2002 Warren Togami <warren@togami.com> 6.0.69-1
- cosmetic fix to RH special case
- update to 6.0.69 (final release candidate)
