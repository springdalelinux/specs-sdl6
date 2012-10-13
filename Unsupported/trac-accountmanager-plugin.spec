%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pybasever: %global pybasever %(%{__python} -c "import sys ; print sys.version[:3]" || echo 0.0)}

%global svnrev  12157
%global svndate 20121012

Name:           trac-accountmanager-plugin
Version:        0.11
Release:        0.2.%{svndate}svn%{svnrev}%{?dist}
Summary:        Trac plugin for account registration and management
Group:          Applications/Internet
License:        Copyright only
URL:            http://trac-hacks.org/wiki/AccountManagerPlugin
Source0:        accountmanagerplugin_%{version}-r%{svnrev}.tar.bz2
Source1:        pull-from-svn.sh
Patch0:         TracAccountManager-0.3dev-r9591-tests.patch
Patch1:         TracAccountManager-0.3dev-r9591-genshi06.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

# This is needed for the test suite
BuildRequires:  trac >= 0.12

# This package is explicitly for trac 0.12.x
Requires:       trac >= 0.12

# Required for import of pkg_resources
Requires:       python-setuptools

# Need at least this version
%if 0%{?rhel}
Requires:       python-genshi06
%else
Requires:       python-genshi >= 0.6
%endif

%description
The AccountManagerPlugin offers several features for managing user accounts:
 * allow users to register new accounts
 * login via an HTML form instead of using HTTP authentication
 * allow existing users to change their passwords or delete their accounts
 * send a new password to users who've forgotten their password
 * administer user accounts using the trac web interface


%prep
%setup -n accountmanagerplugin -q

# Fix broken test suite
#%patch0 -p1

# Make sure we can find Genshi >= 0.6 on EL-6, where it's in an egg
#%patch1 -p1


%build
#cd %{version}
cd trunk
%{__python} setup.py build


%install
rm -rf %{buildroot}
#cd %{version}
cd trunk
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Don't need to package this
rm %{buildroot}%{python_sitelib}/acct_mgr/locale/.placeholder


#%check
#cd %{version}
#%{__python} setup.py test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#%doc %{version}/README %{version}/contrib/sessionstore_convert.py
%doc trunk/README trunk/contrib/sessionstore_convert.py
%dir %{python_sitelib}/acct_mgr/
%{python_sitelib}/acct_mgr/*.py*
%{python_sitelib}/acct_mgr/htdocs/
%{python_sitelib}/acct_mgr/templates/
%dir %{python_sitelib}/acct_mgr/locale/
#%dir %{python_sitelib}/acct_mgr/locale/de/
#%dir %{python_sitelib}/acct_mgr/locale/de/LC_MESSAGES/
#%lang(de) %{python_sitelib}/acct_mgr/locale/de/LC_MESSAGES/acct_mgr.mo
#%dir %{python_sitelib}/acct_mgr/locale/es/
#%dir %{python_sitelib}/acct_mgr/locale/es/LC_MESSAGES/
#%lang(es) %{python_sitelib}/acct_mgr/locale/es/LC_MESSAGES/acct_mgr.mo
#%dir %{python_sitelib}/acct_mgr/locale/ja/
#%dir %{python_sitelib}/acct_mgr/locale/ja/LC_MESSAGES/
#%lang(ja) %{python_sitelib}/acct_mgr/locale/ja/LC_MESSAGES/acct_mgr.mo
#%dir %{python_sitelib}/acct_mgr/locale/ru/
#%dir %{python_sitelib}/acct_mgr/locale/ru/LC_MESSAGES/
#%lang(ru) %{python_sitelib}/acct_mgr/locale/ru/LC_MESSAGES/acct_mgr.mo
%{python_sitelib}/TracAccountManager-*.egg-info/


%changelog
* Fri Oct 12 2012 Thomas Uphill <uphill@ias.edu> - 0.11-r12157
- update for trac 1.0 and spamplugin compatability

* Fri Dec 24 2010 Paul Howarth <paul@city-fan.org> - 0.3-0.2.20101206svn9591
- Require python-genshi >= 0.6 or python-genshi06 as per trac itself
- Go to great trouble to set %%lang on translations
- Help setup.py find Genshi 0.6, which is in an egg for EPEL-6
- Add %%check section and run test suite
- Patch out errors in test suite
- BR: trac for trac.test, needed for test suite

* Tue Dec 14 2010 Paul Howarth <paul@city-fan.org> - 0.3-0.1.20101206svn9591
- Update to current svn snapshot (from trunk for trac 0.12)
- Require trac >= 0.12
- Require python-genshi >= 0.5 as per setup.py

* Fri Dec 10 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.1-0.5.20090522svn5836
- Rebuild for new trac

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2.1-0.4.20090522svn5836
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Aug 28 2009 Ben Boeckel <MathStuf@gmail.com> - 0.2.1-0.3.20090522svn5836
- Remove comments
- Fix tarball

* Thu Aug 27 2009 Ben Boeckel <MathStuf@gmail.com> - 0.2.1-0.2.20090522svn5836
- Merge spec with Paul Howarth's

* Thu Aug 06 2009 Ben Boeckel <MathStuf@gmail.com> - 0.2.1-0.1.20090522svn5836
- Initial package
