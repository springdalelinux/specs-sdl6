Summary: Automatic mail answering program
Name: vacation
Version: 1.2.7.0
Release: 7%{?dist}
License: BSD
Group: Applications/System
Source: http://downloads.sourceforge.net/vacation/%{name}-%{version}.tar.gz
Source1: license-clarification
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: smtpdaemon
URL: http://sourceforge.net/projects/vacation/
BuildRequires: gdbm-devel

%description 
Vacation is the automatic mail answering program found
on many Unix systems.

%description	-l de
Vacation beantwortet automatisch alle eingehenden EMails
mit einer Standard-Antwort und ist auf vielen Unix-Systemen
vorhanden.

%prep
%setup -q
cp -p %SOURCE1 .

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -D -p -m 755 vacation        $RPM_BUILD_ROOT%{_bindir}/vacation
install -D -p -m 755 vaclook         $RPM_BUILD_ROOT%{_bindir}/vaclook
install -D -p -m 444 vacation.man    $RPM_BUILD_ROOT%{_mandir}/man1/vacation.1
install -D -p -m 444 vaclook.man     $RPM_BUILD_ROOT%{_mandir}/man1/vaclook.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/vacation
%{_bindir}/vaclook
%{_mandir}/*/*
%doc COPYING README README.smrsh ChangeLog license-clarification

%changelog
* Wed Aug 05 2009 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 1.2.7.0-7
- changed license to BSD as upstream told me
  (corresponding mail is included in doc).

* Mon Aug 03 2009 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 1.2.7.0-6
- changed license to GPLv2 until licensing is clarified with upstream
- changed source URL to "downloads" instead of "download".
  (bz #474802)

* Mon Jul 06 2009 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 1.2.7.0-5
- Fixes according comments from bz #474802

* Wed Jun 24 2009 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 1.2.7.0-4
- repackaged for Fedora 11.
- Fixed bugs from bz #474802

* Fri Dec 05 2008 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 1.2.7.0-1
- Upgraded to 1.2.7.0
- repackaged for Fedora 10.

* Tue Sep 03 2002 Pete O'Hara <pete@guardiandigital.com>
- Version 1.2.7.rc1, Release 1.2.1
  - Upgraded to 1.2.7.rc1

* Mon Aug 26 2002 Pete O'Hara <pete@guardiandigital.com>
- Version 1.2.6.1, Release 1.2.0
  - Initial release for Mail Suite

* Sun Nov 11 2001 Devon <devon@tuxfan.homeip.net>
- upgrade to version 1.2.7.rc1
* Sat Nov 10 2001 Devon <devon@tuxfan.homeip.net>
- upgrade to version 1.2.6
* Wed Sep 19 2001 Devon <devon@tuxfan.homeip.net>
- added %%post link /etc/smrsh to /usr/bin/vacation
- added %%postun deletion of /etc/smrsh/vacation
- defined a umask of 022 fix permissions on created files.
  $HOME/.forward was created group writable, smrsh refused
  to run in that case. See vacation-1.2.2-permissions.patch

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- fix specfile and patch file to rebuilt

* Mon Aug 07 2000 Michael Stefaniuc <mstefani@redhat.com>
- upgraded to 1.2.2
- fixed security fix

* Wed Aug 02 2000 Than Ngo <than@redhat.de>
- fix manpath (Bug #15070)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Sun Jul 16 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add security fix

* Mon Jul 10 2000 Than Ngo <than@redhat.de>
- fix problem (it won't include the .vacation.msg) (bug #13572)
- use RPM macros

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun May 28 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man pages in correct place
- cleanup specfile
- fix Summary

* Fri Dec 10 1999 Ngo Than <than@redhat.de>
- initial RPM for powertools-6.2
