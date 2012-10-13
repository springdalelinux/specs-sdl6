%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname fssm
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: File system state monitor
Name: rubygem-%{gemname}
Version: 0.2.6.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/ttilley/fssm
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = 1.8
Requires: rubygems
BuildRequires: ruby(abi) = 1.8
BuildRequires: rubygems
# Use rspec-core until rspec are not migrated to RSpec 2.x
BuildRequires: rubygem(rspec-core)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The File System State Monitor keeps track of the state of any number of paths
and will fire events when said state changes (create/update/delete).
FSSM supports using FSEvents on MacOS (with ruby 1.8), Inotify on GNU/Linux,
and polling anywhere else. 


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --force --rdoc %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/

rm %{buildroot}/%{geminstdir}/.gitignore

%check
pushd .%{geminstdir}

# Remove Bundler dependency
sed -i '4,+1d' spec/spec_helper.rb

rspec spec/
popd

%clean

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib/
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.markdown
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{geminstdir}/example.rb
%{geminstdir}/%{gemname}.gemspec
%{geminstdir}/Gemfile
%{geminstdir}/Rakefile
%{geminstdir}/profile/
%{geminstdir}/spec/
%doc %{gemdir}/doc/%{gemname}-%{version}

%changelog
* Tue Apr 05 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.6.1-1
- Updated to fssm 0.2.6.1
- Removed obsolete BuildRoot.
- Removed unnecessary cleanup.
- Testsuite executed using RSpec 2.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.2-3
- Removed explicit RubyGems version

* Fri Dec 17 2010 Vít Ondruch <vondruch@redhat.com> - 0.2.2-2
- Documentation moved into subpackage

* Fri Dec 17 2010 Vít Ondruch <vondruch@redhat.com> - 0.2.2-1
- Initial package
