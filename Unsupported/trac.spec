%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           trac
Version:        1.0
Release:        1%{?dist}
Summary:        Enhanced wiki and issue tracking system
Group:          Applications/Internet
License:        BSD
URL:            http://trac.edgewall.com/
Source0:        http://ftp.edgewall.com/pub/trac/Trac-%{version}.tar.gz
Source1:        trac.conf
Source2:        trac.ini
Source3:        trac.ini-environment_sample
Source4:        %{name}-README.fedora
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-genshi06
BuildRequires:  python-setuptools-devel
Requires:       python-setuptools
Requires:       python-genshi06
Requires:       httpd
Provides:       trac-webadmin = trac-webadmin-0.1.2-0.7.dev_r4429.fc11
Obsoletes:      trac-webadmin < trac-webadmin-0.1.2-0.6
Patch0:         0001-Make-sure-we-use-the-right-python-genshi.patch

%description
Trac is an integrated system for managing software projects, an
enhanced wiki, a flexible web-based issue tracker, and an interface to
the Subversion revision control system.  At the core of Trac lies an
integrated wiki and issue/bug database. Using wiki markup, all objects
managed by Trac can directly link to other issues/bug reports, code
changesets, documentation and files.  Around the core lies other
modules, providing additional features and tools to make software
development more streamlined and effective.

%prep
%setup -q -n Trac-%{version}
#%patch0 -p1
find contrib -type f -exec chmod -x '{}' \;
# don't package windows specific files
rm -f contrib/trac-post-commit-hook.cmd
%{__cp} -a %{SOURCE4} README.fedora

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

# --skip-build causes bad stuff in siteconfig.py as of 0.8.4
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_var}/www/cgi-bin
mv contrib/cgi-bin/trac.*cgi $RPM_BUILD_ROOT%{_var}/www/cgi-bin

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/trac.conf
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/trac/trac.ini
install -Dpm 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/trac/trac.ini-environment_sample
install -dpm 755 $RPM_BUILD_ROOT/etc/trac/{plugin,template}s.d

find sample-plugins/ -type f -name '*.py' -exec install -pm 644 '{}' $RPM_BUILD_ROOT/etc/trac/plugins.d \;

find sample-plugins/ -type f -name '*.ini*' -exec install -pm 644 '{}' $RPM_BUILD_ROOT/etc/trac/ \;

install -dm 755 $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT{%{_bindir}/tracd,%{_sbindir}/tracd}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL README README.fedora RELEASE THANKS UPGRADE contrib/
%{_bindir}/trac-admin
%{_sbindir}/tracd
%{python_sitelib}/*
%config(noreplace) /etc/httpd/conf.d/trac.conf
%dir /etc/trac
%config(noreplace) /etc/trac/*
%{_var}/www/cgi-bin/trac.cgi
%{_var}/www/cgi-bin/trac.fcgi

%changelog
* Fri Dec 10 2010 Jesse Keating <jkeating@redhat.com> - 0.12.1-4
- Update the trac-README.fedora content for global ini

* Tue Dec 07 2010 Jesse Keating <jkeating@redhat.com> - 0.12.1-3
- Build 0.12.1 on el6, patched to use python-genshi06

* Fri Oct 15 2010 Jesse Keating <jkeating@redhat.com> - 0.12.1-2
- Fix README.fedora installation

* Tue Oct 12 2010 Jesse Keating <jkeating@redhat.com> - 0.12.1-1
- Update to 0.12.1

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.11.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Mar 10 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.11.7-1
- New upstream release (including security fix)

* Sat Mar 06 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.11.6-3
- don't package Windows commit hook
- package now includes trac.test module

* Sun Jan 24 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.11.6-2
- add missing setuptools requirement
- removed python-sqlite requirement as Python 2.6 already contains a suitable
  module in the standard library
- removed dependencies on subversion and python-pygments as these are actually
  optional
- added README.fedora to explain which packages can be installed for 
  additional functionality

* Sat Dec 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.11.6-1
- New upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 05 2009 Jesse Keating <jkeating@redhat.com> - 0.11.4-1
- New upstream release to fix bugs and minor enhancements.

* Tue Mar 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.11.3-4
- Fix unowned directory (#473989)

* Mon Mar 09 2009 Jesse Keating <jkeating@redhat.com> - 0.11.3-3
- Obsolete trac-webadmin, its now built in

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.3-1
- Trac 0.11.3 contains a number of bug fixes and minor enhancements.
- The following list contains only a few highlights:
- 
-  * Compatibility with Python 2.6 (#7876, #7458)
-  * PostgreSQL db backend improvement (#4987, #7600)
-  * Highlighting of search results is more robust (#7324, #7830)
-  * Unicode related fixes (#7672, #7959, #7845, #7935, #8024)
-  * Fixed Trac link rendering in ReST (#7712)
- 
- You can find a more detailed release note at:
- http://trac.edgewall.org/wiki/TracDev/ReleaseNotes/0.11

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.11.2.1-4
- Rebuild for Python 2.6

* Fri Nov 28 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2.1-3
- Add dependency on python-pygments
- Rebuild for Python 2.6

* Tue Nov 18 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2.1-2
- Upload new sources
- Add new files to CVS

* Tue Nov 18 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2.1-0.1
- Update to 0.11.2.1

* Mon Jun 23 2008 Ryan B. Lynch <ryan.b.lynch@gmail.com> - 0.11-1
- Update to 0.11

* Sun Jun 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.5-1
- Update to 0.10.5

* Thu Jan  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.4-2
- Simplify files section so that it picks up the egg info files.

* Thu May  3 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.4-1
- Update to 0.10.4

* Mon Mar 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.3.1-2
- Switch requires back to python-sqlite

* Sat Mar 10 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.3.1-1
- Update to 0.10.3.1 to fix security bug

* Sun Jan  7 2007 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 0.10.3-2
- change req: python-sqlite -> python-sqlite2

* Tue Jan  2 2007 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 0.10.3
- upstream release 0.10.3 (#221162)

* Sat Dec  9 2006 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 0.10.3
- rebuild for python 2.5, add python-devel to BR

* Tue Nov 28 2006 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 0.10.2
- upstream release 0.10.2 (#217539)

* Sat Nov 11 2006 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 0.10.1
- upstream release 0.10.1 (fixes CSRF vulnerability, bugzilla #215077)

* Thu Sep 28 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.10
- upstream release 0.10 'Zengia'

* Wed Aug 30 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.6-3
- remove %%ghost for .pyo files; bugzilla #205439

* Wed Aug 30 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.6-2
- rebuild for Fedora Extras 6

* Thu Jul  6 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.6-1
- upstream release 0.9.6

* Tue Apr 18 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.5-1
- bug fix release 0.9.5

* Wed Feb 15 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.4-1
- 0.9.4
 * Deletion of reports has been fixed.
 * Various encoding issues with the timeline RSS feed have been fixed.
 * Fixed a memory leak when syncing with the repository.
 * Milestones in the roadmap are now ordered more intelligently.
 * Fixed bugs: 
   1064, 1150, 2006, 2253, 2324, 2330, 2408, 2430, 2431, 2459, 2544, 
   2459, 2481, 2485, 2536, 2544, 2553, 2580, 2583, 2606, 2613, 2621, 
   2664, 2666, 2680, 2706, 2707, 2735

* Mon Feb 13 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.3-5
- Rebuild for Fedora Extras 5

* Mon Jan 16 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.3-4
- updated trac.conf to allow for trac.*cgi 

* Mon Jan 16 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.3-3
- re-added tracd and trac.fcgi by user request.

* Tue Jan 10 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.3-2
- removed trac.fcgi (bugzilla #174546, comment #11)
- applied patch (bugzilla #174546, attachment id=123008)

* Mon Jan  9 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.3-1
- 0.9.3
- removed tracd (bugzilla #174546, comment #6)
- added trac.conf for httpd
- removed %%{python_sitelib}/trac/test.py
- removed comments

* Tue Dec  6 2005 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.2-2
- added /etc/init.d/tracd
- added /etc/sysconfig/tracd

* Tue Dec  6 2005 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.2-1
- 0.9.2
- fixes SQL Injection Vulnerability in ticket search module.
- fixes broken ticket email notifications.

* Sat Dec  3 2005 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9.1-1
- 0.9.1
- fixes SQL Injection Vulnerability

* Tue Nov 29 2005 Joost Soeterbroek <fedora@soeterbroek.com> - 0.9-1
- Rebuild for Fedora Extras

* Tue Nov  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.9-1
- 0.9.

* Mon Jun 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.4-0.1
- 0.8.4.
- Move tracd to %%{_sbindir} and man page to section 8.

* Thu Jun 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.3-0.1
- 0.8.3.

* Wed Jun  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.2-0.1
- 0.8.2.

* Sun May 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2
- Rebuild for FC4.

* Fri Apr  8 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.1
- First build.
