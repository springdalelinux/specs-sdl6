%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           nltk
Version:        2.0.1rc1
Release:        1%{?dist}
Summary:        Natural Language Toolkit

Group:          Development
License:        GPL
URL:            http://www.nltk.org/download
Source0:        nltk-2.0.1rc1.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:  python PyYAML
Requires:       python PyYAML

%description
Natural Language Toolkit

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/%{name}
%{python_sitelib}/*.egg-info


%changelog
* Fri Mar 16 2011 Benjamin Rose <benrose@cs.princeton.edu>
- Initial release
