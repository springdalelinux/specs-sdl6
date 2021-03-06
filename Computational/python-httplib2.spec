%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name:           python-httplib2
Version:        0.7.2
Release:        1%{?dist}
Summary:        A comprehensive HTTP client library

Group:          System Environment/Libraries
License:        MIT
URL:            http://code.google.com/p/httplib2/
Source0:        http://httplib2.googlecode.com/files/httplib2-%{version}.tar.gz
#Patch0:         httplib_py26.diff
Patch1:         python-httplib2.certfile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-setuptools-devel
BuildRequires: python-devel
BuildArch: noarch

%description
A comprehensive HTTP client library that supports many features left out of
other HTTP libraries.

%prep
%setup -q -n httplib2-%{version}
#%patch0 -p0 -b .issue39
%patch1 -p0 -b .certfile

%build
CFLAGS="$RPM_OPT_FLAGS" python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/*

%changelog
* Fri Feb 24 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.2-1
- Upstream update to 0.7.2
  Which may fixed http://code.google.com/p/httplib2/issues/detail?id=62
  Note this version uses fedora's cert file bundle instead of httplib2
  default.

* Fri Jul 29 2011 Ding-Yi Chen <dchen at redhat.com>  - 0.4.0-5
- Apply that address python-httplib2 (GoogleCode Hosted) issue 39
  http://code.google.com/p/httplib2/issues/detail?id=39

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.0-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Tom "spot" Callaway <tcallawa@redhat.com>
- minor spec cleanups
- enable python3 support

* Fri Apr 02 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.6.0-1
- version upgrade (#566721)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-2
- Rebuild for Python 2.6

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.4.0-1
- initial version
