%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:             submin
Version:          2.0.3
Release:          1%{?dist}
Summary:          Web-based admin interface for svn repositories
Source0:          http://supermind.nl/submin/current/submin-%{version}.tar.gz
License:          Other
Url:              http://supermind.nl/submin/
Group:            Applications/Internet
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    python-devel
BuildArch:	  noarch
Requires:         httpd subversion

%description
Submin provides a web-based admin interface to your svn repositories. features include:
- User/group management
- User/group permissions management per path
- SVN repositories creation
- Config files for apache2 cgi and wsgi created automatically
- Authentication via htpasswd/svn authz
- Authentication synced to svn (and trac)

%prep
%setup -q

%build
env CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc IMPORTING INSTALL LICENSE copying
%{_bindir}/submin2-admin
%{_mandir}/man1/submin2-admin*
%{python_sitearch}/*egg-info
%dir %{python_sitearch}/submin
%{python_sitearch}/submin/*

%changelog
* Tue Feb 21 2012 Josko Plazonic <plazonic@math.princeton.edu> - 2.0.3-1
- initial build
