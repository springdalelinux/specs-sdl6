# Generated from sexp_processor-3.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname sexp_processor
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: A branch of ParseTree providing generic sexp processing tools
Name: rubygem-%{gemname}
Version: 3.0.4
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubyforge.org/projects/parsetree/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygem(rake)
BuildRequires: rubygem(hoe)
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
sexp_processor branches from the ParseTree gem bringing all the generic sexp
processing tools with it. Sexp, SexpProcessor, Environment, etc... all
for your language processing pleasure.

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

# Drop the standalone mode - won't run that way due to missing rubygems require
# anyway
find %{buildroot}%{geminstdir}/test -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
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
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 3.0.4-3
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 3.0.4-1
- New upstream version - 1 minor enhancement.

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 3.0.3-1
- Initial package
