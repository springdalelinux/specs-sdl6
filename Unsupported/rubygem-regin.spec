%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname regin
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Ruby Regexp Introspection
Name: rubygem-%{gemname}
Version: 0.3.8
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/josh/%{gemname}
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
# git clone https://github.com/josh/regin.git && cd regin && git checkout v0.3.8
# tar czvf regin-tests.tgz spec/
Source1: %{gemname}-tests.tgz
Requires: ruby(abi) = %{rubyabi}
Requires: rubygems
Requires: ruby
BuildRequires: rubygems
BuildRequires: ruby
# Use rspec-core until rspec are not migrated to RSpec 2.x
BuildRequires: rubygem(rspec-core)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Regin allows you to introspect on Ruby Regexps. Powered by an over the top
regexp syntax parser written in racc/rexical.


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

%clean

%check
mkdir %{_tmppath}/%{gemname}-%{version}
tar xzvf %{SOURCE1} -C %{_tmppath}/%{gemname}-%{version}

pushd %{_tmppath}/%{gemname}-%{version}
RUBYOPT="-I%{buildroot}%{geminstdir}/lib" rspec spec/
popd

rm -rf %{_tmppath}/%{gemname}-%{version}

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Mon Nov 7 2011 Steve Linabery <slinaber@redhat.com> - 0.3.8-2
- Bump release to avoid conflict with previously checked in but unbuilt 0.3.8-1

* Wed Apr 06 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.8-1
- Updated to Regin 0.3.8

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.7-2
- Removed obsolete cleanup from install and clean sections

* Wed Jan 19 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.7-1
- Initial package
