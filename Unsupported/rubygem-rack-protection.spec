# Generated from rack-protection-1.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gemname rack-protection

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: You should use protection!
Name: rubygem-%{gemname}
Version: 1.1.4
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/rkh/rack-protection
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
Requires: rubygem(rack) 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildRequires(check): rubygem(rspec)
BuildRequires(check): rubygem(rspec-core)
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(rack)
BuildRequires(check): rubygem(rack-test)
BuildRequires(check): rubygem(bundler)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
You should use protection!


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

%check
#export GEM_PATH=$(pwd)/%{gemdir}
pushd .%{geminstdir}

rake test --trace


%files
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/License
%{geminstdir}/README.md
%{geminstdir}/Rakefile
%{geminstdir}/rack-protection.gemspec
%{geminstdir}/spec

%changelog
* Wed Oct 26 2011 Josko Plazonic - 1.1.4-1
- Initial package
