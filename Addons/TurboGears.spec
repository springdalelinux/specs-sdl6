%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           TurboGears
Version:        1.1.3
Release:        2%{?dist}
Summary:        Back-to-front web development in Python

Group:          Development/Languages
License:        MIT
URL:            http://www.turbogears.org
Source0:        http://pypi.python.org/packages/source/T/%{name}/%{name}-%{version}.tar.gz
Source1:        porting-1.0-1.1.txt
Patch0:         %{name}-1.0.8-cherrypyreq.patch
# Reported upstream http://trac.turbogears.org/ticket/2419
Patch1: turbogears-sqlcreate.patch
Patch2: turbogears-feed.patch
# Backport upstream commit r7389
Patch3: turbogears-httponly.patch
# Patch to allow turbogears to work with old turbokid until/unless RHEL6
# updates
Patch100: TurboGears-old-turbokid.patch
# Patch so TurboGears detects the correct version of dependencies installed on the system
Patch101: turbogears-pkg-resources-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-configobj
BuildRequires: python-formencode
BuildRequires: python-genshi
BuildRequires: python-kid
BuildRequires: python-paste-script
BuildRequires: python-peak-rules
BuildRequires: python-simplejson
BuildRequires: python-tgmochikit
BuildRequires: python-turbocheetah
BuildRequires: python-sqlobject
BuildRequires: python-sqlalchemy
BuildRequires: python-elixir
BuildRequires: python-toscawidgets
BuildRequires: python-tw-forms
BuildRequires: python-nose
BuildRequires: python-webtest
BuildRequires: python-dateutil

%if 0%{?fedora} || 0%{?rhel} > 5
Requires:       python-cherrypy2
BuildRequires:  python-cherrypy2
%else
BuildRequires:  python-elementtree >= 1.2.6
# EPEL-5 shipped < 2.3.0 originally
# Note there is also a requirement for this to be cherrypy 2, however 
# cherrypy 3 should only turn up as a parallel installable version...
BuildRequires:  python-cherrypy >= 2.3.0
Requires:       python-elementtree >= 1.2.6
Requires:       python-cherrypy >= 2.3.0
%endif
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: python-turbojson >= 1.3
Requires: python-turbojson >= 1.3
BuildRequires: python-turbokid >= 1.0.5
Requires:       python-turbokid >= 1.0.5
%else
# Note: This package is needed until/unless RHEL6 updates to
# python-turbojson-1.3 or later
BuildRequires: python-turbojson13
Requires:       python-turbojson13
# Need newer versions of python-turbokid (in RHEL6 base) but:
# The newer version is to fix a bug where kid templates will not be reloaded
# when they've changed.  That should only affect code that's being developed,
# not code that's simply being served
BuildRequires: python-turbokid >= 1.0.4
Requires:       python-turbokid >= 1.0.4
%endif

Requires:       python-sqlobject >= 0.10.1
Requires:       python-formencode >= 1.2.1
Requires:       python-setuptools >= 0.6c11
Requires:       python-turbocheetah >= 1.0
Requires:       python-simplejson >= 1.9.1
Requires:       python-paste-script >= 1.7
Requires:       python-configobj >= 4.3.2
Requires:       python-nose >= 0.9.3
Requires:       python-psycopg2
Requires:       python-elixir >= 0.6.1
Requires:       python-genshi >= 0.4.4
Requires:       python-kid
Requires:       python-peak-rules
Requires:       python-tgmochikit
Requires:       python-toscawidgets >= 0.9.6
Requires:       python-tw-forms >= 0.9.6
Requires:       python-webtest
Requires:       python-dateutil

%description
TurboGears brings together four major pieces to create an easy to install, easy
to use web megaframework. It covers everything from front end (MochiKit
JavaScript for the browser, Genshi for templates in Python) to the controllers
(CherryPy) to the back end (SQLAlchemy).

The TurboGears project is focused on providing documentation and integration
with these tools without losing touch with the communities that already exist
around those tools.

TurboGears is easy to use for a wide range of web applications.


%prep
%setup -q
%patch0 -b .cherrypyreq
%patch1 -p1 -b .sqlcreate
%patch2 -p1 -b .feed
%patch3 -p3 -b .httponly
%if 0%{?rhel} && 0%{?rhel} >= 6
%patch100 -p1 -b .deps
%endif
%patch101 -p1 -b .pkgresources

cp -p %{SOURCE1} .

%build
sed -i 's/.*TurboJson.*//' TurboGears.egg-info/requires.txt
%{__python} setup.py egg_info
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check
cp %{_bindir}/nosetests .
sed -i 's/__requires__ =\(.*\)/__requires__ = [\1, "TurboGears"]/' nosetests 

PYTHONWARNINGS=default PYTHONPATH=$(pwd) ./nosetests -q

# fails {
#PYTHONWARNINGS=default PYTHONPATH=$(pwd) python setup.py test
# }

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc CHANGELOG.txt LICENSE.txt porting-1.0-1.1.txt
%attr(0755,root,root) %{_bindir}/tg-admin
%{python_sitelib}/%{name}-%{version}-py*.egg-info/
%{python_sitelib}/turbogears/

%changelog
* Fri Jul 15 2011 Toshio Kuratomi <toshio@feoraproject.org> - 1.1.3-2
- Patch backported from upstream to add support for marking session cookie
  httponly

* Fri Jul 15 2011 Toshio Kuratomi <toshio@feoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Tue Jul 5 2011 Toshio Kuratomi <toshio@feoraproject.org> - 1.1.2-5
- Add patches for building with SQLalchemy-0.7.1 and python-2.7.2
  https://bugzilla.redhat.com/show_bug.cgi?id=715760

* Sat Jun 25 2011 Toshio Kuratomi <toshio@feoraproject.org> - 1.1.2-4
- Add __requires__ to quickstart templates.  This is mitigation for
  https://bugzilla.redhat.com/show_bug.cgi?id=670223

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.2-2
- Changes to allow the package to run on RHEL6.
- Add a text file with tips for porting from 1.0 to 1.1

* Sat Dec 25 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.2-1
- Update to upstream 1.1.2
- Add python-dateutil as a a Req (for scheduler)

* Thu Dec 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.1-1
- Update to upstream 1.1.1
- Fix test case failure
- Fix problem with an import not matching what's actually called.

* Thu Sep 16 2010 Mark Chappell <tremble@fedoraproject.org> - 1.0.9-7
- Add explicit versions to ensure we install cleanly on EL-5 RHBZ#451228

* Tue Aug 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.9-6
- Fix building on python-2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.9-4
- Fix failing unittest with SA-0.6

* Wed Jan 13 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.9-3
- Fix deprecation warnings

* Thu Dec 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.9-2
- Update sql create patch for traceback when used in development mode RHBZ#548594

* Mon Nov 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9 bugfix release.
- Paginate fix is in upstream.

* Mon Nov 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.8-8
- Fix problem with sql create and sqlobject

* Mon Aug 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.8-7
- Update Requires conditionals so we can share with EPEL

* Tue Aug 11 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.8-6
- Add patch to make FeedController work when the default template engine is
  not kid.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> - 1.0.8-4
- Remove python-json as a requirement

* Sat May 2 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.8-3
- Fix from upstream for pagination problem.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 03 2009 Luke Macken <lmacken@redhat.com> - 1.0.8-1
- Latest upstream release.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.7-3
- Rebuild for Python 2.6

* Wed Sep 17 2008 Luke Macken <lmacken@redhat.com> 1.0.7-2
- Add a patch to allow newer versions of TurboJson

* Tue Sep 16 2008 Luke Macken <lmacken@redhat.com> 1.0.7-1
- Update to the latest upstream release
- Utilize the test suite
- Remove the setup.py patch

* Tue May 27 2008 Luke Macken <lmacken@redhat.com> 1.0.4.4-3
- Patch our setup.py to remove the hard version requirements for SQLObject.
  This has changed upstream as well.

* Tue Mar 11 2008 Luke Macken <lmacken@redhat.com> 1.0.4.4-2
- Add TurboGears-1.0.4.4-cherrypyreq.patch to explicitly require the
  appropriate version of CherryPy when necessary.

* Fri Mar  7 2008 Luke Macken <lmacken@redhat.com> 1.0.4.4-1
- Update to 1.0.4.4
- Remove the setuptools and sqlalchemy-backport patches

* Fri Feb 29 2008 Luke Macken <lmacken@redhat.com> 1.0.4.3-3
- Require python-paste-script >= 1.6.2 (Bug #435525)

* Thu Feb 21 2008 Toshio Kuratomi <tkuratom@redhat.com> 1.0.4.3-2
- Fixes for SQLAlchemy-0.4 and exceptions.  Upstream Bug #1721.

* Fri Feb  1 2008 Luke Macken <lmacken@redhat.com> 1.0.4.3-1
- 1.0.4.3

* Sat Jan 26 2008 Luke Macken <lmacken@redhat.com> 1.0.4.2-3
- Require Genshi and Elixir

* Wed Jan 23 2008 Luke Macken <lmacken@redhat.com> 1.0.4.2-2
- Update setuptools patch to work with the CherryPy egg_info

* Tue Jan 22 2008 Luke Macken <lmacken@redhat.com> 1.0.4.2-1
- 1.0.4.2

* Sun Jan 20 2008 Luke Macken <lmacken@redhat.com> 1.0.4-1
- 1.0.4
- Remove paginate patch
- Update setuptools patch

* Sat Dec 15 2007 Luke Macken <lmacken@redhat.com> 1.0.3.2-7
- Add TurboGears-1.0.3.2-paginate.patch backported from upstream
  http://trac.turbogears.org/ticket/1629

* Sat Oct 27 2007 Luke Macken <lmacken@redhat.com> 1.0.3.2-6
- Remove python-TestGears requirement, as this functionality
  has been replaced by nose.

* Mon Oct 8 2007 Toshio Kuratomi <a.badger@gmail.com> 1.0.3.2-5
- Update patch so that quickstart template pulls in the proper sqlalchemy
  when tg-admin quickstart -s is run.

* Fri Oct 5 2007 Toshio Kuratomi <a.badger@gmail.com> 1.0.3.2-4
- Require sqlalchemy 0.3.

* Thu Sep 27 2007 Toshio Kuratomi <a.badger@gmail.com> 1.0.3.2-3
- Update setuptools patch to modify quickstart template for compat eggs as well.

* Mon Sep 24 2007 Luke Macken <lmacken@redhat.com> 1.0.3.2-2
- Update setuptools patch to "fix" CherryPy dependency error

* Mon Sep 13 2007 Luke Macken <lmacken@redhat.com> 1.0.3.2-1
- 1.0.3.2
- Remove etree patch

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> 1.0.2.2-3
- Update for python-setuptools changes in rawhide

* Thu May 11 2007 Luke Macken <lmacken@redhat.com> 1.0.2.2-2
- Update etree patch to work with Python2.4
- Update setuptools patch

* Thu May 3 2007 Luke Macken <lmacken@redhat.com> 1.0.2.2-1
- 1.0.2.2
- TurboGears-1.0.2.2-etree.patch to use xml.etree instead of elementtree module

* Fri Jan 26 2007 Toshio Kuratomi <toshio@tiki-lounge.com> 1.0.1-2
- Don't flub the patch this time.

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> 1.0.1-1
- Upgrade to upstream 1.0.1.
- Update the setuptools patch.
- Conditionalize python-elementtree as python-2.5 provides it.
- Include rather than ghosting *.pyo.
- Require python-psycopg2 instead of psycopg, TurboGears + psycopg2 supports
  unicode whereas psycopg does not.
- Make all files except tg-admin non-executable.

* Fri Jan 19 2007 Luke Macken <lmacken@redhat.com> 1.0b2-6
- Add python-elementtree to BuildRequires

* Tue Dec 12 2006 Luke Macken <lmacken@redhat.com> 1.0b2-5
- Rebuild for new elementtree

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 1.0b2-4
- Add python-devel to BuildRequires

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 1.0b2-3
- Rebuild for python 2.5

* Sat Dec  2 2006 Luke Macken <lmacken@redhat.com> 1.0b2-2
- Update the setuptools patch

* Sat Dec  2 2006 Luke Macken <lmacken@redhat.com> 1.0b2-1
- 1.0b2

* Fri Nov 21 2006 Luke Macken <lmacken@redhat.com> 1.0b1-3
- Add python-TestGears back to Requires

* Fri Nov 21 2006 Luke Macken <lmacken@redhat.com> 1.0b1-2
- Add python-psycopg to Requires

* Mon Sep 11 2006 Luke Macken <lmacken@redhat.com> 1.0b1-1
- 1.0b1

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> 0.8.9-4
- Rebuild for FC6

* Sun Jul  9 2006 Luke Macken <lmacken@redhat.com> 0.8.9-3
- Require python-TestGears (bug #195370)

* Thu Jul 6 2006 Luke Macken <lmacken@redhat.com> 0.8.9-2
- Add TurboGears-0.8.9-setuptools.patch

* Thu Jul 6 2006 Luke Macken <lmacken@redhat.com> 0.8.9-1
- Bump to 0.8.9
- Remove TurboGears-0.8a5-optim.patch and TurboGears-0.8a5-setuptools.patch

* Sat Feb 18 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8a5-1
- Initial RPM release
