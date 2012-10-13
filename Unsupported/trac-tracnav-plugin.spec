%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global tarname TracNav-%{version}

Name:           trac-tracnav-plugin
Version:        4.1
Release:        4%{?dist}
Summary:        Navigation Bar for Trac
Group:          Applications/Internet
License:        GPLv2+
URL:            http://svn.ipd.uka.de/trac/javaparty/wiki/TracNav
Source:         http://pypi.python.org/packages/source/T/TracNav/TracNav-%{version}.zip
Patch0:         tracnav-4.1-trac-0.12-compat.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
Requires:       python-setuptools
Requires:       trac >= 0.11

%description
The TracNav macro implements a fully customizable navigation bar for
the Trac wiki engine. The contents of the navigation bar is a wiki
page itself and can be edited like any other wiki page through the web
interface. The navigation bar supports hierarchical ordering of
topics. The design of TracNav mimics the design of the TracGuideToc
that was originally supplied with Trac.


%prep
%setup -n %{tarname} -q
# from r3276
%patch0 -p0


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README
%{python_sitelib}/*


%changelog
* Fri Jan  7 2011 Thomas Moschny <thomas.moschny@gmx.de> - 4.1-4
- Add patch from upstream for Trac 0.12 compatibility.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 31 2009 Thomas Moschny <thomas.moschny@gmx.de> - 4.1-2
- Use %%global instead of %%define.

* Mon Jul 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 4.1-1
- New package.
