%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-cherrypy2
Version:        2.3.0
Release:        11%{?dist}
Summary:        A pythonic, object-oriented web development framework
Group:          Development/Libraries
License:        BSD
URL:            http://www.cherrypy.org/
Source0:        http://download.cherrypy.org/cherrypy/%{version}/CherryPy-%{version}.tar.gz
Source1:        README.fedora
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:         python-cherrypy-tutorial-doc.patch
Patch1:         python-cherrypy-2.3.0-EINTR.patch
Patch2:         python-cherrypy-2.3.0-py26-test.patch
Patch3:         python-cherrypy-deprecation.patch

BuildArch:      noarch

BuildRequires:  python-devel
%if 0%{?fedora} && 0%{?fedora} <= 12
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

Requires: python-setuptools

%description
CherryPy allows developers to build web applications in much the same way 
they would build any other object-oriented Python program. This usually 
results in smaller source code developed in less time.

This is a compat package for programs which still need the 2.x branch of
CherryPy.

%prep
%setup -q -n CherryPy-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .depr

%{__sed} -i 's/\r//' CHANGELOG.txt README.txt CHERRYPYTEAM.txt cherrypy/tutorial/README.txt
cp -p %{SOURCE1} .

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' bdist_egg

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
easy_install -m --prefix $RPM_BUILD_ROOT%{_usr} dist/*.egg
find $RPM_BUILD_ROOT%{python_sitelib}/ -type f -exec chmod -x \{\} \;

%check
cd cherrypy/test
%{__python} test.py --dumb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt CHERRYPYTEAM.txt README.txt README.fedora
%doc cherrypy/tutorial
%{python_sitelib}/*

%changelog
* Fri Dec 4 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.0-11
- Fix deprecation warnings.
- Change setuptools BuildRequirement as we're back to one package in F-13.

* Wed Aug 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.0-10
- Remove the touch of easy_install.pth.  It's not necessary and leads to file
  conflicts with other packages.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-7
- Build against the python-2.6 target

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-6
- Set tests to be non-interactive via the commandline instead of a patch.
- Patch to fix test errors with Python-2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3.0-5
- Rebuild for Python 2.6

* Sat Jun 14 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-4
- Update README.fedora to fix some code examples and confusing wording.

* Wed Jan 16 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-3
- Merge changes from current python-cherrypy package.
- Update to 2.3.0.

* Wed Jan 16 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.2.1-9
- Initial cherrypy2 build.

* Sun Jan  6 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.2.1-8
- Fix a security bug with a backport of http://www.cherrypy.org/changeset/1775
- Include the egginfo files as well as the python files.

* Sat Nov  3 2007 Luke Macken <lmacken@redhat.com> 2.2.1-7
- Apply backported fix from http://www.cherrypy.org/changeset/1766
  to improve CherryPy's SIGSTOP/SIGCONT handling (Bug #364911).
  Thanks to Nils Philippsen for the patch.

* Mon Feb 19 2007 Luke Macken <lmacken@redhat.com> 2.2.1-6
- Disable regression tests until we can figure out why they
  are dying in mock.

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-5
- Add python-devel to BuildRequires

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-4
- Rebuild for python 2.5

* Mon Sep 18 2006 Luke Macken <lmacken@redhat.com> 2.2.1-3
- Rebuild for FC6
- Include pyo files instead of ghosting them

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-2
- Rebuild

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-1
- Update to 2.2.1
- Remove unnecessary python-abi requirement

* Sat Apr 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.2.0-1
- Update to 2.2.0

* Wed Feb 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.1.1-1
- Update to 2.1.1 (Security fix)

* Tue Nov  1 2005 Gijs Hollestelle <gijs@gewis.nl> 2.1.0-1
- Updated to 2.1.0

* Sat May 14 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-2
- Added dist tag

* Sun May  8 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-1
- Updated to 2.0.0 final
- Updated python-cherrypy-tutorial-doc.patch to match new version

* Wed Apr  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.0.0-0.2.b
- Removed CFLAGS

* Wed Mar 23 2005 Gijs Hollestelle <gijs[AT]gewis.nl> 2.0.0-0.1.b
- Initial Fedora Package
