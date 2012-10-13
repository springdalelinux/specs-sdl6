# fedora says they defined sitearch, so we'll use that.
#%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define appname netgroup

Summary: Python modules for querying netgroup information
Name: python-%{appname}
Version: 0.11
Release: 1.PU_IAS.2
Source0: http://planetjoel.com/viewarticle/629/Python+NSS+netgroups+interface/%{name}.%{version}.tar.gz

License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: python-netgroup = %{version}
BuildRequires: gettext
BuildRequires: python-devel

%description
python nss netgroups module

%prep
%setup -q -n %{appname}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE
%{python_sitearch}/%{appname}.so
%{python_sitearch}/Netgroup-1.0-py2.6.egg-info

%changelog
* Tue Apr 17 2012 Thomas Uphill <uphill@ias.edu> - 0.11
- rebuild for 6
- change to python_sitearch

* Wed Oct 21 2009 Thomas Uphill <uphill@ias.edu> - 0.11
- initial build
