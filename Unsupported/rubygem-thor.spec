# Generated from thor-0.12.0.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname thor
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Scripting framework that replaces rake, sake and rubigen
Name: rubygem-%{gemname}
Version: 0.14.6
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/wycats/thor
Source0: http://rubygems.org/download/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(ruby2ruby)
Requires: rubygem(ParseTree)
Requires: rubygem(rake)
Requires: rubygem(diff-lcs)
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
#BuildRequires(check): rubygem(rspec)
# No rdoc or fakeweb gem packages yet
#BuildRequires(check): rubygem(rake), rubygem(diff-lcs), rubygem(rdoc), rubygem(fakeweb)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Thor is a scripting framework that replaces rake, sake and rubigen.

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
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

%clean
rm -rf %{buildroot}

# Commented out until we have rspec ~> 2.1 in Fedora.
# We'll also have to add a patch removing the simplecov
# dependency until ruby 1.9 is in Fedora
#%check
#pushd %{buildroot}%{geminstdir}
#rspec spec

# Can't yet run %%check missing a couple dependencies
#%check
#pushd .%{geminstdir}
#ruby -Ilib bin/thor :spec

%files
%defattr(-,root,root,-)
%{_bindir}/thor
%{_bindir}/rake2thor
%doc %{geminstdir}/CHANGELOG.rdoc
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.md
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Thorfile
%{geminstdir}/spec
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Mohammed Morsi <mmorsi@redhat.com> - 0.14.6-1
- Updated to latest upstream version

* Wed May 5 2010 Matthew Kent <mkent@magoazul.com> - 0.13.6-1
- New upstream version.

* Fri Dec 18 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-2
- Add Requires for rubygem(rake) (#542559).
- Upstream replaced Source after the gemcutter migration, update to latest
  (#542559).
- Add Requires for rubygem(diff-lcs) as Thor can take advantage of it for
  colourized diff output (#542559).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-1
- Initial package
