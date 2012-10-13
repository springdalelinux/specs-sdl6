# Generated from ZenTest-4.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ZenTest
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Automated test scaffolding for Ruby
Name: rubygem-%{gemname}
Version: 4.3.3
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.zenspider.com/ZSS/Products/ZenTest/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires(check): rubygem(rake), rubygem(hoe), rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
ZenTest is an automated test scaffolding for Ruby that provides 4 different
tools: zentest, unit_diff, autotest and multiruby. These tools can be used for
test conformance auditing and rapid XP.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%build
mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod 0755

# Various files marked executable that shouldn't be, and remove needless
# shebangs
find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'
find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/local/bin/ruby"#!/usr/bin/ruby"'
find %{buildroot}%{geminstdir}/test -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{geminstdir} -type f | \
  xargs chmod 0644
find %{buildroot}%{geminstdir}/bin -type f | \
  xargs chmod 0755

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
rake test

%files
%defattr(-,root,root,-)
%{_bindir}/autotest
%{_bindir}/multigem
%{_bindir}/multiruby
%{_bindir}/multiruby_setup
%{_bindir}/unit_diff
%{_bindir}/zentest
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/test
%{geminstdir}/.autotest
%{geminstdir}/articles
%{geminstdir}/example*.rb
%{geminstdir}/example.txt
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Thu Aug 26 2010 Matthew Kent <mkent@magoazul.com> - 4.3.3-1
- New upstream version. Minor fixes and enhancements.

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 4.3.1-1
- New upstream version. Minor bugfixes - 1.9 compatibility.

* Sun Jan 24 2010 Matthew Kent <mkent@magoazul.com> - 4.2.1-1
- New upstream version.
- Don't reorganize files, leave as upstream intended.

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-3
- Drop Requires on hoe, only used by Rakefile (#539442).
- Move Rakefile to -doc (#539442).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-2
- Better Source (#539442).
- More standard permissions on files.

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-1
- Initial package
