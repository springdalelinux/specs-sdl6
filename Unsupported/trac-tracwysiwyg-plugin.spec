%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define plugin tracwysiwyg
%define svnrev 7774

Name:           trac-%{plugin}-plugin
Version:        0.11
Release:        1.%{svnrev}%{?dist}
Summary:        TracWiki WYSIWYG Editor Plugin
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/TracWysiwygPlugin
# source got from http://trac-hacks.org/changeset/latest/tracwysiwygplugin?old_path=/&filename=tracwysiwygplugin&format=zip
Source0:        %{plugin}plugin-r%{svnrev}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac, python-setuptools

%description
TracWiki WYSIWYG Editor Plugin 

%prep
%setup -n %{plugin}plugin/0.11 -q


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
* Wed May 20 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build, used Fedora's trac-ticketdelete-plugin.spec as the base
