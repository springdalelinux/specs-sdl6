# Generated from erubis-2.6.5.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname erubis
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: A fast and extensible eRuby implementation
Name: rubygem-%{gemname}
Version: 2.6.6
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.kuwata-lab.com/erubis/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(abstract) >= 1.0.0
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygem(abstract)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Erubis is a very fast, secure, and extensible implementation of eRuby.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep

%build

%install
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --bindir %{buildroot}%{_bindir} \
            --force --rdoc %{SOURCE0}

# Wrong filename - reported upstream via
# http://rubyforge.org/tracker/?func=detail&aid=27330&group_id=1320&atid=5201
mv %{buildroot}%{geminstdir}/test/data/users-guide/Example.ejava \
  %{buildroot}%{geminstdir}/test/data/users-guide/example.ejava

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

find %{buildroot}%{geminstdir}/{bin,contrib} -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

find %{buildroot}%{geminstdir}/benchmark -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env ruby/d'

%check
export GEM_PATH=%{buildroot}%{gemdir}
export PATH=%{buildroot}%{_bindir}:$PATH

pushd %{buildroot}%{geminstdir}
RUBYOPT="rubygems" ruby test/test.rb

%files
%defattr(-,root,root,-)
%{_bindir}/erubis
%doc %{geminstdir}/CHANGES.txt
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/README.txt
%dir %{geminstdir}

# We install via gem
%exclude %{geminstdir}/setup.rb

%{geminstdir}/bin
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/benchmark
%{geminstdir}/test
%{geminstdir}/examples
%{geminstdir}/contrib

# Prefer generated rdoc
%exclude %{geminstdir}/doc-api

%{geminstdir}/doc
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Feb 14 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.6-1
- Updated to the latest upstream (#670589).
- Removed flawed require check.
- Removed obsolete BuildRoot.
- Removed obsolete cleanup.
- Package setup and test execution reworked.
- Removed bindir magick.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 29 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-2
- Move file rename to build stage (#530275).
- Simplify %%check stage (#530275).
- Remove disable of test_syntax2, fixed by new ruby build (#530275).

* Mon Oct 19 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-1
- Initial package
