%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define plugin privatewiki
%define svnrev 5810

Name:           trac-%{plugin}-plugin
Version:        0.11
Release:        2.%{svnrev}%{?dist}
Summary:        Allows you to protect Trac wiki pages against access
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/TracWysiwygPlugin
# source got from http://trac-hacks.org/changeset/latest/privatewikiplugin?old_path=/&filename=privatewikiplugin&format=zip
Source0:        %{plugin}plugin-r%{svnrev}.zip
Patch1:		privatewikiplugin-fixuser.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac, python-setuptools

%description
Allows you to protect Trac wiki pages against access

%prep
%setup -n %{plugin}plugin/0.11 -q
%patch1 -p2 -b .fixuser


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
# skip-build doesn't work on el4
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*


%changelog
* Fri Mar 12 2010 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild with local tweak that allows anon users access

* Wed May 20 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build, used Fedora's trac-ticketdelete-plugin.spec as the base
