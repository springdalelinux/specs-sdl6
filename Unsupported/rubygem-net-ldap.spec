# Generated from net-ldap-0.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gemname net-ldap

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Net::LDAP for Ruby (also called net-ldap) implements client access for the Lightweight Directory Access Protocol (LDAP), an IETF standard protocol for accessing distributed directory services
Name: rubygem-%{gemname}
Version: 0.2.2
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://net-ldap.rubyforge.org/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby >= 1.8.7
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby >= 1.8.7
BuildRequires(check): rubygem(hoe)
BuildRequires(check): rubygem(metaid)
BuildRequires(check): rubygem-flexmock
BuildRequires(check): rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Net::LDAP for Ruby (also called net-ldap) implements client access for the
Lightweight Directory Access Protocol (LDAP), an IETF standard protocol for
accessing distributed directory services. Net::LDAP is written completely in
Ruby with no external dependencies. It supports most LDAP client features and
a
subset of server features as well.
Net::LDAP has been tested against modern popular LDAP servers including
OpenLDAP and Active Directory. The current release is mostly compliant with
earlier versions of the IETF LDAP RFCs (2251–2256, 2829–2830, 3377, and
3771).
Our roadmap for Net::LDAP 1.0 is to gain full <em>client</em> compliance with
the most recent LDAP RFCs (4510–4519, plus portions of 4520–4532).


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
rm -rf %{buildroot}%{geminstdir}/{.autotest,.gemtest,.rspec,Rakefile,autotest,%{gemname}.gemspec,spec,test,testserver}

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
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/Contributors.rdoc
%doc %{geminstdir}/Hacking.rdoc
%doc %{geminstdir}/History.rdoc
%doc %{geminstdir}/License.rdoc
%doc %{geminstdir}/README.rdoc


%changelog
* Wed Oct 26 2011 Josko Plazonic - 0.2.2-1
- Initial package
