# Generated from rubycas-server-1.0.gem by gem2rpm -*- rpm-spec -*-
%global gemname rubycas-server

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Provides single sign-on authentication for web applications using the CAS protocol
Name: rubygem-%{gemname}
Version: 1.0
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://code.google.com/p/rubycas-server/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
Requires: rubygem(activerecord) => 2.3.6
Requires: rubygem(activerecord) < 2.4
Requires: rubygem(activesupport) => 2.3.6
Requires: rubygem(activesupport) < 2.4
Requires: rubygem(sinatra) => 1.0
Requires: rubygem(sinatra) < 2
Requires: rubygem(gettext) => 2.1.0
Requires: rubygem(gettext) < 2.2
Requires: rubygem(crypt-isaac) => 0.9.1
Requires: rubygem(crypt-isaac) < 0.10
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
#BuildRequires(check): rubygem(rspec)
#BuildRequires(check): rubygem(rake)
#BuildRequires(check): rubygem(bundler)
#BuildRequires(check): git
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Provides single sign-on authentication for web applications using the CAS
protocol.


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
            --bindir .%{_bindir} \
            --force %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x
rm -rf %{buildroot}%{geminstdir}/{Gemfile,Rakefile,rubycas-server.gemspec,setup.rb,spec}

#%check
##export GEM_PATH=$(pwd)/%{gemdir}
#pushd .%{geminstdir}
#
#rake test --trace

%files
%dir %{geminstdir}
%{_bindir}/rubycas-server
%{geminstdir}/bin
%{geminstdir}/lib
%{geminstdir}/po
%{geminstdir}/public
%{geminstdir}/resources
%{geminstdir}/tasks
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.md

%changelog
* Wed Oct 26 2011 Josko Plazonic - 1.0-1
- Initial package
