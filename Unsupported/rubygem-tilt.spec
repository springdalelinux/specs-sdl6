%global gemname tilt

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Generic interface to multiple Ruby template engines
Name: rubygem-%{gemname}
Version: 1.3.2
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/rtomayko/%{gemname}
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
# Fixes rhbz#715713
# https://github.com/rtomayko/tilt/issues/93
Patch0: Fix-compilesite-test-for-multiple-threads.patch
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems)
Requires: ruby
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(RedCloth)

# Markaby test fails. It is probably due to rather old version found in Fedora.
# https://github.com/rtomayko/tilt/issues/96
# BuildRequires: rubygem(markaby)

# RDiscount test fails. Is it due to old version in Fedora?
# BuildRequires: rubygem(rdiscount)

BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Generic interface to multiple Ruby template engines


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
            --bindir .%{_bindir} \
            --force %{SOURCE0}

pushd .%{geminstdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x
find %{buildroot} -name .yardoc -exec rm -rf '{}' \; || :

%check
pushd %{buildroot}%{geminstdir}
RUBYOPT="rubygems Ilib" testrb test/*_test.rb
popd
find %{buildroot} -name .sass-cache -exec rm -rf '{}' \; || :

%files
%{_bindir}/%{gemname}
%exclude %{geminstdir}/%{gemname}.gemspec
%{geminstdir}/bin
%{geminstdir}/lib
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/README.md
%doc %{geminstdir}/TEMPLATES.md
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%{geminstdir}/Rakefile
%doc %{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/test


%changelog
* Wed Jul 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.2-1
- Updated to the tilt 1.3.2.
- Test suite for erubis, haml, builder and RedCloth template engines enabled.

* Fri Jun 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Fixes FTBFS (rhbz#715713).

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Test moved to doc subpackage
- %{gemname} macro used whenever possible.

* Mon Feb 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Initial package
