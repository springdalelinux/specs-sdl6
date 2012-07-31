%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-sqlobject
Version:        0.10.2
Release:        5%{?dist}
Summary:        SQLObject -Object-Relational Manager, aka database wrapper  

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://sqlobject.org/
Source0:        http://cheeseshop.python.org/packages/source/S/SQLObject/SQLObject-%{version}.tar.gz  
Patch0:         %{name}-%{version}-setup.patch
Patch1:         %{name}-deprecation.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
Requires:       python-sqlite2, python-formencode >= 0.2.2
Requires:       MySQL-python, postgresql-python


%description
Classes created using SQLObject wrap database rows, presenting a
friendly-looking Python object instead of a database/SQL interface.
Emphasizes convenience.  Works with MySQL, Postgres, SQLite, Firebird.

This package requires sqlite. Futher database connectors have to be
installed separately.

%prep
%setup -q -n SQLObject-%{version}
%patch0 -b .setup
%patch1 -p1 -b .depr

%build
%{__python} setup.py build
chmod 0644 docs/rebuild

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc PKG-INFO README.txt docs

%{python_sitelib}/*
%{_bindir}/*

%changelog
* Fri Jan 8 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10.2-5
- Fix deprecation warnings https://bugzilla.redhat.com/show_bug.cgi?id=552463

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10.2-2
- Rebuild for Python 2.6

* Thu Jun 26 2008 Luke Macken <lmacken@redhat.com> 0.10.2-1
- Update to 0.10.2
- Add {MySQL,postgresql}-python to Requires

* Tue May 13 2008 Luke Macken <lmacken@redhat.com> 0.10.1-1
- Update to 0.10.1

* Tue Mar 11 2008 Luke Macken <lmacken@redhat.com> 0.10.0-1
- Update to 0.10.0

* Thu Mar  6 2008 Luke Macken <lmacken@redhat.com> 0.9.4-1
- Update to 0.9.4
- Add python-sqlobject-0.9.4-setup.patch to prevent it from trying to download
  its own version of setuptools automatically.

* Thu Feb 21 2008 Toshio Kuratomi <tkuratom@redhat.com> 0.9.3-2
- Stop deleting the ez_setup directory so we can build setuptools eggs as
  upstream intends.

* Wed Feb 13 2008 Toshio Kuratomi <tkuratom@redhat.com> 0.9.3-1
- Update to 0.9.3
- Pick up egginfo on rawhide.

* Tue Nov 27 2007 Luke Macken <lmacken@redhat.com> 0.9.2-1
- 0.9.2

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> 0.9.1-1
- 0.9.1

* Sat Jun  2 2007 Luke Macken <lmacken@redhat.com> 0.9.0-1
- Latest upstream release

* Thu May  3 2007 Luke Macken <lmacken@redhat.com> 0.8.2-1
- 0.8.2

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> 0.7.3-1
- 0.7.3

* Mon Dec 18 2006 Luke Macken <lmacken@redhat.com> 0.7.2-3
- Require python-sqlite2

* Tue Dec 12 2006 Luke Macken <lmacken@redhat.com> 0.7.2-2
- Add python-devel to BuildRequires

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> 0.7.2-1
- 0.7.2
- Remove python-sqlobject-admin.patch, python-sqlobject-0.7.0-ordered-deps.patch
  and python-sqlobject-0.7.0-pkg_resources.patch

* Mon Sep 11 2006 Luke Macken <lmacken@redhat.com> 0.7.0-8
- python-sqlobject-0.7.0-ordered-deps.patch from upstream ticket
  http://trac.turbogears.org/turbogears/ticket/279 (Bug #205894)

* Fri Sep  8 2006 Luke Macken <lmacken@redhat.com> 0.7.0-7
- Include pyo files instead of ghosting them
- Rebuild for FC6

* Sun Jun  9 2006 Luke Macken <lmacken@redhat.com> 0.7.0-6
- Add python-sqlobject-0.7.0-pkg_resources.patch (Bug #195548)
- Remove unnecessary python-abi requirement

* Sun Oct 23 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.7.0-5.fc4
- fixed the changelog usage of a macro

* Sun Oct 23 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.7.0-4.fc4
- %%{?dist} for further distinguish the different builts.

* Tue Oct 13 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.7.0-3
- fixed a spelling error reported by rpmlint
- changed the installation to use -O1
- %%ghost'ed the the resulting *.pyo files

* Tue Oct 06 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.7.0-2
- fixed requirement for FormEncode >= 0.2.2
- Upgrade to upstream version 0.7.0

* Tue Sep 20 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.7-0.1.b1
- Version 0.7b1
