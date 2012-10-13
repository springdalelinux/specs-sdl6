# Generated from sass-3.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gemname sass

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: A powerful but elegant CSS compiler that makes CSS fun again
Name: rubygem-%{gemname}
Version: 3.1.4
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://sass-lang.com/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Patch1: rubygem-sass-3.1.4-fix-util-require.patch
Patch2: rubygem-sass-3.1.4-fix-cache_stores-require.patch
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems)
Requires: rubygem(fssm)
Requires: ruby
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: rubygem(rake)
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Sass makes CSS fun again. Sass is an extension of CSS3, adding
nested rules, variables, mixins, selector inheritance, and more.
It's translated to well-formatted, standard CSS using the
command line tool or a web-framework plugin.


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
gem install --local --install-dir .%{gemdir} --bindir .%{_bindir} \
            --force %{SOURCE0}

pushd .%{geminstdir}
rm .yardopts
rm -rf vendor
%patch1
%patch2

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%check
pushd %{buildroot}%{geminstdir}
rake test
rm -rf .sass-cache

%files
%dir %{geminstdir}
%{_bindir}/sass
%{_bindir}/sass-convert
%{geminstdir}/bin
%{geminstdir}/lib
%{geminstdir}/init.rb
%{geminstdir}/rails/init.rb
%{geminstdir}/extra/update_watch.rb
%{geminstdir}/VERSION
%{geminstdir}/VERSION_NAME
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/CONTRIBUTING
%doc %{geminstdir}/README.md
%doc %{geminstdir}/test
%doc %{geminstdir}/Rakefile
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 3.1.4-4
- Add patches to make sass work in Fedora

* Thu Jul 21 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-3
- changed ruby(fssm) dep to rubygem(fssm)

* Thu Jul 14 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-2
- corrected license, whitespace fixes

* Wed Jul 13 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.4-1
- Initial package
