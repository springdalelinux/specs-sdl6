%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup}

%define	module	numexpr

Summary:	Fast numerical array expression evaluator for Python and NumPy
Name:		python-%{module}
Version:	1.4.1
Release:	3%{?dist}
Source0:	http://numexpr.googlecode.com/files/%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Languages
URL:		http://numexpr.googlecode.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	numpy >= 1.4.1
BuildRequires:	numpy >= 1.4.1
BuildRequires:	python-devel


%description
The numexpr package evaluates multiple-operator array expressions many
times faster than NumPy can. It accepts the expression as a string,
analyzes it, rewrites it more efficiently, and compiles it to faster
Python code on the fly. It's the next best thing to writing the
expression in C and compiling it with a specialized just-in-time (JIT)
compiler, i.e. it does not require a compiler at runtime.

%prep
%setup -q -n %{module}-%{version}

sed -i "s|/usr/bin/env |/usr/bin/|" %{module}/cpuinfo.py

%build
python setup.py build 

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build  --root=%{buildroot}
#This could be done more properly ?
chmod 0755 %{buildroot}%{python_sitearch}/%{module}/cpuinfo.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ANNOUNCE.txt LICENSE.txt RELEASE_NOTES.txt README.txt
%{python_sitearch}/numexpr/
%{python_sitearch}/numexpr-%{version}-py*.egg-info/

%changelog
* Fri Apr 29 2011 Thibault North <tnorth@fedoraproject.org> - 1.4.1-3
- Fix buildroot issue

* Tue Dec 21 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-2
- Fixes for the review process

* Wed Nov 05 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-1
- Initial package based on Mandriva's one

