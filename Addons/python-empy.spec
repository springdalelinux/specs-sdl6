%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global tarname empy

Name:           python-empy
Version:        3.3
Release:        5%{?dist}
Summary:        A powerful and robust template system for Python

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.alcyone.com/software/empy/
Source:         http://www.alcyone.com/software/%{tarname}/%{tarname}-latest.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-setuptools, python-devel

%description
EmPy is a system for embedding Python expressions and statements in template
text; it takes an EmPy source file, processes it, and produces output. 

%prep
%setup -q -n %{tarname}-%{version}

#fix shebang on rpmlint
sed -i -e '1d' em.py

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README version.txt
%{python_sitelib}/*


%changelog
* Wed Mar 03 2010 Filipe Rosset <rosset.filipe@gmail.com> - 3.3-5
- Fix compilation error

* Mon Mar 01 2010 Filipe Rosset <rosset.filipe@gmail.com> - 3.3-4
- Fix license

* Sat Feb 27 2010 Filipe Rosset <rosset.filipe@gmail.com> - 3.3-3
- Remove python-devel in BuildRequires
- Fix shebang on rpmlint

* Tue Feb 23 2010 Filipe Rosset <rosset.filipe@gmail.com> - 3.3-2
- Add build information

* Mon Jan 11 2010 Filipe Rosset <rosset.filipe@gmail.com> - 3.3-1
- Initial RPM release
