%define major_version 1.2
%define minor_version 6

%define shortname 389-ds
%define pkgname   dirsrv

Name: 389-ds-console
Version: %{major_version}.%{minor_version}
Release: 1%{?dist}
Summary: 389 Directory Server Management Console

Group: Applications/System
License: GPLv2
URL: http://port389.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source: http://port389.org/sources/%{name}-%{version}.tar.bz2
Requires: 389-admin
BuildRequires: ant >= 1.6.2
BuildRequires: ldapjdk
BuildRequires: idm-console-framework >= 1.1
BuildRequires: java-devel >= 1:1.6.0
%if 0%{?rhel} < 6
ExcludeArch: ppc
%endif


%description
A Java based remote management console used for managing 389
Directory Server.  The 389 Console is required to load and
run these jar files.

%package          doc
Summary:          Web docs for 389 Directory Server Management Console
Group:            Documentation
Requires:         %{name} = %{version}-%{release}

%description      doc
Web docs for 389 Directory Server Management Console

%prep
%setup -q
                                                                                
%build
%{ant} \
    -Dconsole.location=%{_javadir} \
    -Dbuilt.dir=`pwd`/built

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
install -m644 built/package/%{shortname}* $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
install -d $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/slapd/help
install -m644 help/en/*.html $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/slapd
install -m644 help/en/tokens.map $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/slapd
install -m644 help/en/help/*.html $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/slapd/help

# create symlinks
pushd $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
ln -s %{shortname}-%{version}.jar %{shortname}-%{major_version}.jar
ln -s %{shortname}-%{version}.jar %{shortname}.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}-%{major_version}_en.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}_en.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}_en.jar

%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/%{pkgname}/manual/en/slapd
%doc %{_datadir}/%{pkgname}/manual/en/slapd/tokens.map
%doc %{_datadir}/%{pkgname}/manual/en/slapd/*.html
%doc %{_datadir}/%{pkgname}/manual/en/slapd/help/*.html
                                                                                
%changelog
* Fri Jun 17 2011 Rich Megginson <rmeggins@redhat.com> 1.2.6-1
- git tag 389-ds-console-1.2.6
- added skins support
- Bug 700908 - Validate matching rules when creating a new attribute
- Bug 705753 - Refresh problem in Console directory browser

* Wed Mar 30 2011 Rich Megginson <rmeggins@redhat.com> 1.2.5-1
- the 1.2.5 release - git tag 389-ds-console-1.2.5
- Bug 616707 - Add attribute matching rule UI to Console
- Bug 533505 - Warn about CA cert trust when enabling SSL in Console
- Bug 158262 - Windows Sync UI is inconistent
- Bug 504803 - Allow nsslapd-*-logmaxdiskspace to be set to -1 in UI
- Bug 474113 - Allow access log level to be configured from Console
- Bug 229693 - Update naming attribute when objectclass is removed
- Bug 211296 - Clean up all HTML pages (Admin Express, Repl Monitor, etc)

* Wed Feb 23 2011 Rich Megginson <rmeggins@redhat.com> 1.2.4-1
- the 1.2.4 release - git tag 389-ds-console-1.2.4
- Bug 450016 - RFE- Console display values in KB/MB/GB
- Bug 387981 - plain files can be chosen on the Restore Directory dialog
- Bug 661116 - 389-console Configuration tab admin permissions (nsslapd-referral ?) and folder not expending immediatly
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- Bug 553066 - Directory Console: do not display "subtree" index type
- Bug 599732 - Root node in directory browser shows DN syntax error

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 13 2010 Rich Megginson <rmeggins@redhat.com> 1.2.3-1
- the 1.2.3 release

* Fri Apr 30 2010 Rich Megginson <rmeggins@redhat.com> 1.2.2-1
- the 1.2.2 release

* Thu Apr 15 2010 Rich Megginson <rmeggins@redhat.com> 1.2.1-1
- the 1.2.1 release

* Fri Dec 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-6
- Excluding PPC for EPEL builds as there is not openjdk there

* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> 1.2.0-5
- final rebuild for 1.2.0 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Rich Megginson <rmeggins@redhat.com> 1.2.0-3
- added doc subpackage

* Fri May 15 2009 Rich Megginson <rmeggins@redhat.com> 1.2.0-2
- rename to 389

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.2.0-1
- this is the 1.2.0 release

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-1
- this is the 1.1.3 release

* Thu Sep  4 2008 Rich Megginson <rmeggins@redhat.com> 1.1.2-2
- fixed incorrect source

* Thu Jul  3 2008 Rich Megginson <rmeggins@redhat.com> 1.1.2-1
- fix threading issues with create new ds instance dialog

* Wed Apr 16 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-3
- use java-devel > 1.5.0 for build requires

* Tue Jan 22 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-2
- resolves bug 429421
- had incorrect source - new source has been uploaded

* Thu Jan 10 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-1
- changes for fedora package review
- added requires for icedtea java
- added LICENSE

* Wed Dec 19 2007 Rich Megginson <rmeggins@redhat.com> 1.1.0-5
- This is for the Fedora DS 1.1 release

* Mon Aug 13 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-4
- Added online help files to package. Use pkgname for filesystem
  path naming instead of shortname.

* Wed Aug  1 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-3
- Updated build requirement for new console framework package.
Updated install location and Admin Server dependency. Also did
some specfile cleanup.

* Mon Jul 30 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-2
- Updated requirements.

* Mon Nov 14 2005 Nathan Kinder <nkinder@redhat.com> 1.1.0-1
- Initial creation
