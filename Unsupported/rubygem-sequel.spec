# Generated from sequel-3.16.0.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(/usr/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(/usr/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname sequel
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: The Database Toolkit for Ruby
Name: rubygem-%{gemname}
Version: 3.16.0
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://sequel.rubyforge.org
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(abi) = 1.8
Requires: rubygems
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The Database Toolkit for Ruby

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
/usr/bin/gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/sequel
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/COPYING
%{gemdir}/gems/%{gemname}-%{version}/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/doc

%changelog
* Thu Nov 04 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-6
- Change License to MIT

* Wed Oct 27 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-5
- Fixed duplicated version on change log entry

* Tue Oct 26 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-4
- renamed spec file name
- change from list of doc files to doc folder 
* Fri Oct 23 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-3
- Added Require ruby(abi)=1.8
* Fri Oct 21 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-2
- Broken package into main and doc
* Fri Oct 15 2010 Alejandro Pérez <aeperezt@fedoraproject.org> - 3.16.0-1
- Initial package
