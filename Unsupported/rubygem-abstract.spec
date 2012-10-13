# Generated from abstract-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname abstract
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Allows you to define an abstract method in Ruby
Name: rubygem-%{gemname}
Version: 1.0.0
Release: 3%{?dist}
Group: Development/Languages
License: GPLv2 or Ruby
URL: http://rubyforge.org/projects/abstract
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Small library that allows you to define an abstract method in Ruby.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%build
mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# We have this in specifications/
rm -f %{buildroot}%{geminstdir}/abstract.gemspec

# And we install via gem
rm -f %{buildroot}%{geminstdir}/setup.rb

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
ruby test/test.rb

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/README.txt
%doc %{geminstdir}/ChangeLog
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/test
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2009 Matthew Kent <mkent@magoazul.com> - 1.0.0-2
- Fix license

* Mon Oct 19 2009 Matthew Kent <mkent@magoazul.com> - 1.0.0-1
- Initial package
