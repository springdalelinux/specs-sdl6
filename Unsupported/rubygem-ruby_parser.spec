# Generated from ruby_parser-2.0.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ruby_parser
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: A ruby parser written in pure ruby
Name: rubygem-%{gemname}
Version: 2.0.4
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://parsetree.rubyforge.org/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# These test cases are carried in the ParseTree gem in test/. Carry them here
# rather than attempting to install ParseTree-doc in check and introducing a circular
# dependency
Source1: pt_testcase.rb
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygem(sexp_processor)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygem(rake)
BuildRequires: rubygem(hoe)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(sexp_processor)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
ruby_parser (RP) is a ruby parser written in pure ruby (utilizing
racc - which does by default use a C extension). RP's output is
the same as ParseTree's output: s-expressions using ruby's arrays and
base types.

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

cp -p %{SOURCE1} $(pwd)/%{geminstdir}/test/

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

# Drop the standalone mode for tests - won't run that way due to missing 
# rubygems require anyway. One instance in lib as well
find %{buildroot}%{geminstdir}/{test,lib} -type f | \
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
%{_bindir}/ruby_parse
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
# Script creates a circular dependency and is primarily for development
# Included, but it's dependencies aren't met.
#%{geminstdir}/lib/gauntlet_rubyparser.rb
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/.autotest
%{geminstdir}/test
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 2.0.4-5
- replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 30 2009 Matthew Kent <mkent@magoazul.com> - 2.0.4-3
- Remove exclude for gauntlet_rubyparser.rb, let user deal with dependencies if
  they need it.

* Sun Nov 29 2009 Matthew Kent <mkent@magoazul.com> - 2.0.4-2
- Move pt_testcase.rb to the build stage so it's included in the rpm (#541491).
- Drop version requirements for sexp_processor as it is a new package
  (#541491).
- Exclude gauntlet_rubyparser.rb as it introduces a circular dependency
  (#541491).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 2.0.4-1
- Initial package
