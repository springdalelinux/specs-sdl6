# Generated from net-ssh-2.0.23.gem by gem2rpm -*- rpm-spec -*-

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname net-ssh
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Net::SSH: a pure-Ruby implementation of the SSH2 client protocol
Name: rubygem-%{gemname}
Version: 2.0.23
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/net-ssh/net-ssh
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = 1.8 
Requires: rubygems
BuildRequires: ruby
BuildRequires: rubygems
BuildRequires: rubygem(rake)
BuildRequires: rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: rubygem(mocha)
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%description
Net::SSH: a pure-Ruby implementation of the SSH2 client protocol.


%prep

%build

%install

mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}


            
# file-not-utf8 correction
pushd %{buildroot}%{geminstdir}
iconv --from=ISO-8859-1 --to=UTF-8 THANKS.rdoc > THANKS.rdoc.new && \
touch -r THANKS.rdoc THANKS.rdoc.new && \
mv THANKS.rdoc.new THANKS.rdoc            
popd

# remove gem "test-unit" line
sed -i -e '/test-unit/, 1d' %{buildroot}%{geminstdir}/test/common.rb

%check

pushd %{buildroot}%{geminstdir}
ruby -Ilib -Itest -rrubygems test/test_all.rb
rake test --trace
popd

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%{geminstdir}/support
%exclude %{geminstdir}/setup.rb
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/THANKS.rdoc
%doc %{geminstdir}/CHANGELOG.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Manifest
%{geminstdir}/Rakefile
%{geminstdir}/Rudyfile
%{geminstdir}/test
# Required to run tests
%{geminstdir}/net-ssh.gemspec

%changelog
* Tue Apr 5 2011 Jay Greguske <jgregusk@redhat.com> - 2.0.23-6
- Version bump

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 2.0.23-5
- rebuild to ensure F14 has higher NVR than F13

* Fri Jun 11 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-4
- Bring back the BR: rubygem(rake) and rake test

* Thu Jun 10 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-3
- test command from test/README.txt
- Remove gem "test-unit" line
- Removed Requires rubygem(rake)
- BuildRequires/Requires: rubygem(mocha) for tests

* Thu Jun 10 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-2
- Using %%exclude for setup.rb
- Keeping net-ssh.gemspec for tests
- Moved file-not-utf8 correction to before %%check section

* Wed Jun 09 2010 Shreyank Gupta <sgupta@redhat.com> - 2.0.23-1
- Initial package
