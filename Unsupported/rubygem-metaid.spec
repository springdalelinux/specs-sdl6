# Generated from metaid-1.0.gem by gem2rpm -*- rpm-spec -*-
%global gemname metaid

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: slight metaprogramming helpers
Name: rubygem-%{gemname}
Version: 1.0
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://whytheluckystiff.net/metaid/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
why the lucky stiff

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --force %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/
rm -f %{buildroot}%{geminstdir}/.require_paths

%files
%dir %{geminstdir}
%{geminstdir}/metaid.rb
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Wed Oct 26 2011 Josko Plazonic - 1.0-1
- Initial package
