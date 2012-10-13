# Generated from ruby2ruby-1.2.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ruby2ruby
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Generate pure ruby from RubyParser compatible Sexps
Name: rubygem-%{gemname}
Version: 1.2.4
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://seattlerb.rubyforge.org/ruby2ruby/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# These test cases are carried in the ParseTree gem in test/. Carry them here
# rather than attempting to install ParseTree-doc in check and introducing a circular
# dependency
Source1: pt_testcase.rb
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygem(sexp_processor)
Requires: rubygem(ruby_parser)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires(check): rubygem(rake), rubygem(hoe), rubygem(minitest)
BuildRequires(check): rubygem(sexp_processor), rubygem(ruby_parser)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
ruby2ruby provides a means of generating pure ruby code easily from
RubyParser compatible Sexps. This makes making dynamic language
processors in ruby easier than ever!

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
# rubygems require anyway.
find %{buildroot}%{geminstdir}/test -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
find %{buildroot}%{geminstdir}/lib -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env.*/d'
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
%{_bindir}/r2r_show
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
%{geminstdir}/.autotest
%{geminstdir}/test
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Sun Nov 29 2009 Matthew Kent <mkent@magoazul.com> - 1.2.4-2
- Move pt_testcase.rb to the build stage so it's included in the rpm (#541512).
- Drop version requirements for sexp_processor and ruby_parser as they are new
  packages (#541512).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 1.2.4-1
- Initial package
