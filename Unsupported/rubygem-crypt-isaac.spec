# Generated from crypt-isaac-0.9.1.gem by gem2rpm -*- rpm-spec -*-
%global gemname crypt-isaac

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Ruby implementation of the ISAAC PRNG
Name: rubygem-%{gemname}
Version: 0.9.1
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://rubyforge.org/projects/crypt-isaac
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
ISAAC is a fast, strong random number generator. Details on the algorithm can 
be found here: burtleburtle.net/bob/rand/isaac.html This provides a consistent
and capable algorithm for producing independent streams of quality random 
numbers.


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
rm -rf %{buildroot}%{geminstdir}/{test,setup.rb,%{gemname}.gemspec}

%check
export GEM_PATH=$(pwd)/%{gemdir}
pushd .%{geminstdir}
ls -la
ruby setup.rb test

%files
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/TODO
%doc %{geminstdir}/VERSIONS

%changelog
* Wed Oct 26 2011 Josko Plazonic - 0.9.1-2
- Initial package
