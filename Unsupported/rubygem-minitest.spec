# Generated from minitest-1.4.2.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname minitest
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Small and fast replacement for ruby's huge and slow test/unit
Name: rubygem-%{gemname}
Version: 1.6.0
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubyforge.org/projects/bfts
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires(check): rubygem(rake), rubygem(hoe)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular
test writer and for language implementors that need a minimal set of
methods to bootstrap a working unit test suite.

miniunit/spec is a functionally complete spec engine.

miniunit/mock, by Steven Baker, is a beautifully tiny mock object framework.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

pushd .%{geminstdir}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

find %{buildroot}%{geminstdir}/lib -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{geminstdir} -type f | \
  xargs chmod 0644

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
rake test

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/test
%{geminstdir}/.autotest
%{geminstdir}/design_rationale.rb
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Tue May  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-1
- Update to 1.6.0 (#586505)
- Patch0 removed

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-3
- Drop Requires on hoe, only used by Rakefile (#538303).
- Move Rakefile to -doc (#538303).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-2
- Better Source (#538303).
- More standard permissions on files.

* Tue Nov 17 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-1
- Initial package
