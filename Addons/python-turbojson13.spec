%if !(0%{?fedora} > 12 || 0%{?rhel} >= 6)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global module turbojson

Name:           python-turbojson13
Version:        1.3.2
Release:        1%{?dist}
Summary:        Python template plugin that supports json

Group:          Development/Languages
License:        MIT
URL:            http://cheeseshop.python.org/pypi/TurboJson
Source0:        http://pypi.python.org/packages/source/T/TurboJson/TurboJson-%{version}.tar.gz
# Our peak-rules package has patches that bring it up to the required version
# -- need to patch turbojson so that the metadata there knows this
Patch0:         python-turbojson-peak-rules-compat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-peak-rules >= 0.5a1.dev-8.2582
BuildRequires: python-nose
BuildRequires: python-sqlalchemy
BuildRequires: python-sqlobject

BuildRequires: python-simplejson >= 1.9.1
Requires:      python-simplejson >= 1.9.1

Requires:      python-peak-rules >= 0.5a1.dev-8.2582

%description
This package provides a template engine plugin, allowing you
to easily use Json with TurboGears, Buffet or other systems
that support python.templating.engines.

This package contains version 1.3 of turbjson.

%prep
%setup -q -n TurboJson-%{version}
%patch0 -p1 -b .deps

%build
%{__python} setup.py bdist_egg


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{python_sitelib}
touch %{buildroot}%{python_sitelib}/easy-install.pth
easy_install -m --prefix %{buildroot}%{_usr} dist/*.egg
find %{buildroot}%{python_sitelib} -type f -exec chmod a-x \{\} \;
%{__rm} %{buildroot}%{python_sitelib}/easy-install.pth

%check
python setup.py test

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/*.egg/


%changelog
* Wed Sep 7 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.2-1
- New upstream.  Once again require simplejson because the speed is so much better

* Fri Jul 15 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-2
- Rebuild because the previous build was not added to updates in bodhi

* Tue Feb 3 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-1
- Upstream change to make simplejson optional if running on py2.6 or higher

* Mon Jan 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-2
- New turbojson13 forward compat module for EPEL6 based on the current
  python-turbojson package

* Sun Dec 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-2
- Update spec for minor guidelines changes

* Sun Sep 19 2010 Luke Macken <lmacken@redhat.com> - 1.3-1
- Update to 1.3
- Remove turbojson-result-row-proxy.patch, which is present in this release
- Drop our prioritized_methods requirement
- Require a more recent version of PEAK-Rules
- Pull in SQLAlchemy & SQLObject as BuildRequires to run the test suite

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Feb 8 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.1-9
- Add patch to fix SA RowProxy and ResultProxy
- Update BR for setuptools and defining python_sitelib
- Trim changelog

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.1-7
- And nose

* Tue Mar 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.1-6
- Add BR on simplejson so testsuite will run.

* Tue Mar 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.1-5
- Enable test suite.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.1-3
- Rebuild for Python 2.6

* Wed Sep 17 2008 Luke Macken <lmacken@redhat.com> 1.2.1-2
- Require python-prioritized-methods > 0.2

* Tue Sep 16 2008 Luke Macken <lmacken@redhat.com> 1.2.1-1
- Latest release of the 1.2.x series
- Require python-peak-rules (#459157, #459117)

* Sun Jun 22 2008 Luke Macken <lmacken@redhat.com> 1.2-1
- Latest upstream release, intended to be used with the upcoming TurboGears 1.1 version.
- Remove python-turbojson-SAfix-r3749.patch

* Sat Feb 2 2008 Toshio Kuratomi <tkuratom@redhat.com> 1.1.2-3
- ...and remember to include the patch in cvs.

* Sat Feb 2 2008 Toshio Kuratomi <tkuratom@redhat.com> 1.1.2-2
- Backport fix for 1.1.2's SQLAlchemy breakage.
