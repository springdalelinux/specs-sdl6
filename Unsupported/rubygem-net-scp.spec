%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname net-scp
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: A pure Ruby implementation of the SCP client protocol
Name: rubygem-%{gemname}
Version: 1.0.4
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://net-ssh.rubyforge.org/scp
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: rubygems
Requires: rubygem(net-ssh)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires: rubygem(net-ssh)
BuildRequires: rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A pure Ruby implementation of the SCP client protocol


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep

%build

%install
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

%check
pushd %{buildroot}%{geminstdir}
RUBYOPT="rubygems" ruby test/test_all.rb

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{geminstdir}/Manifest
%{geminstdir}/Rakefile
%{geminstdir}/net-scp.gemspec
%{geminstdir}/setup.rb
%doc %{geminstdir}/CHANGELOG.rdoc
%{geminstdir}/test
%doc %{gemdir}/doc/%{gemname}-%{version}

%changelog
* Thu Dec 08 2011 Steve Linabery <slinaber@redhat.com> - 1.0.4-3
- bump release to avoid conflict with existing distcvs tag

* Thu Mar 17 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.4-2
- Removed obsolete cleanup.
- Removed explicit requires.

* Tue Feb 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.4-1
- Initial package
